from flask import Flask, render_template
import re
import time
from collections import defaultdict
import pywikibot
from pywikibot import pagegenerators
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__) 

sumPatroll = 0
finalStr = ""
overflag = False # 完成标志
executor = ThreadPoolExecutor(3) # 线程池

@app.route('/')
def index():
    Pokemons = []
    Pokemons2 = []
    Pokemons3 = []
    site = pywikibot.Site('zh', 'wikipedia')
    cat = pywikibot.Category(site, "Category:正在等待審核的草稿")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    i = 0
    for page in gen:
        i += 1
        if("<ref" not in page.text):
            Pokemons.append(page.title())
        else:
            if(page.text.count("<ref") == 1):
                Pokemons2.append(page.title())
        Pokemons3.append(page.title())
    return render_template("CatWikiCheck.html", len = len(Pokemons), Pokemons = Pokemons,len2 = len(Pokemons2), Pokemons2 = Pokemons2,len3 = len(Pokemons3), Pokemons3 = Pokemons3, i = i)

@app.route('/ZhWikiCatAfcCheck')
def ZhWikiCatAfcCheck():
    WikiText = []
    site = pywikibot.Site('zh', 'wikipedia')
    cat = pywikibot.Category(site, "Category:正在等待審核的草稿")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    for page in gen:
        WikiText.append(page.text[0:2000])
        WikiText.append("https://zh.wikipedia.org/wiki/" + page.title())
        WikiText.append("\n\n\n\n\n\n\n\n\n\n\n\n")
    return render_template("ZhWikiCatAfcCheck.html", len = len(WikiText), WikiText = WikiText)

@app.route('/patrollInfo')
def patroll():
    executor.submit(patrollInfo)
    return render_template('index.html')

@app.route('/testimg')
def testimg():
    return render_template('test.html')

def patrollInfo():
    site = pywikibot.Site('zh', 'wikipedia')
    gen = site.newpages(namespaces=0, patrolled=False, returndict=True)
    pagetext = ""
    catext = ""
    userlist = defaultdict(int)
    global sumPatroll
    for pageCat, info in gen:
        if not re.search(r'\[\[(Category|分類|分类|category):|{{(Uncategorized|Copyvio|消歧義|Notability|bd)', pageCat.text):
            catext = catext + "[[" + pageCat.title() + "]]、"
        sumPatroll += 1
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
    page.text = "此时共有" + str(sumPatroll) + "条条目未巡查，以下是统计情况：\n\n" + pagetext + "存在潜在问题：\n\n" + catext + "\n\n统计于：" + localtime
    print(page.text)
    global finalStr
    finalStr = page.text
    global overflag
    overflag = True

@app.route('/update', methods=['POST'])
def update():
    global sumPatroll
    if(overflag == False):
        return "此时共有" + str(sumPatroll) + "条条目未巡查";
    if(overflag == True):
        return finalStr;
