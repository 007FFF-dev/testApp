from flask import Flask, render_template
import re
import time
from collections import defaultdict
import pywikibot
from pywikibot import pagegenerators
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__) 

finalStr = ""
overflag = False # 完成标志
executor = ThreadPoolExecutor(3) # 线程池

@app.route('/')
def index():
    site = pywikibot.Site('zh', 'wikipedia')
    cat = pywikibot.Category(site, "Category:正在等待審核的草稿")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    str = ""
    for page in gen:
        if("<ref" not in page.text):
            str = str + page.title() + "\n"
    str = str + "\n以上是【Category:正在等待審核的草稿】中可能需要检查的草稿"
    return str

@app.route('/patrollInfo')
def patroll():
    executor.submit(patrollInfo)
    return render_template('index.html')

def patrollInfo():
    site = pywikibot.Site('zh', 'wikipedia')
    gen = site.newpages(namespaces=0, patrolled=False, returndict=True)
    pagetext = ""
    catext = ""
    userlist = defaultdict(int)
    sum = 0
    for pageCat, info in gen:
        if not re.search(r'\[\[(Category|分類|分类|category):|{{(Uncategorized|Copyvio|消歧義|Notability|bd)', pageCat.text):
            catext = catext + "[[" + pageCat.title() + "]]、"
        sum += 1
        userlist[info['user']] += 1
    userlistcnt = defaultdict(list)
    for user, cnt in userlist.items():
        if cnt <= 1:
            continue
        userlistcnt[cnt].append(user)
    for cnt, users in sorted(userlistcnt.items()):
        pagetext += str(cnt) + "条 "
        pagetext += '、'.join(users) + "\n\n"
    page = pywikibot.Page(site, "User:Air7538/沙盒02")
    localtime = time.asctime(time.localtime(time.time()))
    page.text = "此时共有" + str(sum) + "条条目未巡查，以下是统计情况：\n\n" + pagetext + "存在潜在问题：\n\n" + catext + "\n\n统计于：" + localtime
    print(page.text)
    global finalStr
    finalStr = page.text
    global overflag
    overflag = True

@app.route('/update', methods=['POST'])
def update():
    if(overflag == False):
        return "此时共有" + str(sum) + "条条目未巡查";
    if(overflag == True):
        return finalStr;
