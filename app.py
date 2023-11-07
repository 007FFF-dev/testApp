# -*- coding: utf-8 -*-
#
# This file is part of the Toolforge flask WSGI tutorial
#
# Copyright (C) 2017 Bryan Davis and contributors
# Copyright (C) 2023 David Caro and contributors
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import flask
import pywikibot
from pywikibot import pagegenerators

app = flask.Flask(__name__)
site = pywikibot.Site('zh', 'wikipedia')
cat = pywikibot.Category(site, "Category:正在等待審核的草稿")
gen = pagegenerators.CategorizedPageGenerator(cat)
str = ""

@app.route('/')
def index():
  for page in gen:
    if("<ref" not in page.text):
        str = str + page.title() + "\n"
  str = str + "\n以上是【Category:正在等待審核的草稿】中可能需要检查的草稿"
  return str
