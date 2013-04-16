# -*- coding: utf-8 -*-

import datetime
from bib.models import *
from string import *
import re

def extractPages():
    qs = Article.objects.all()
    cnt = 0
    for q in qs:
        if q.bibliographical_description != '':
            pgs = re.findall('s.\ ?[0-9]+-?[0-9]*,?\ ?[0-9]*-?[0-9]*', q.bibliographical_description)
            if len(pgs) > 0:
                pgs = re.findall('[0-9]+-?[0-9]*', pgs[0])
                for p in pgs:
                    pArray = p.split('-')
                    ap = ArticlePages()
                    ap.article = q
                    ap.page_from = pArray[0]
                    if len(pArray) > 1:
                        ap.page_to = pArray[1]
                    ap.save()
                    cnt += 1
    return cnt