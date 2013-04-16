# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader
from django.db.models import Min
from django.db.models import Q
import re
import datetime

from models import *

templates = {
    'header': 'bazhum/header.html',
    'footer': 'bazhum/footer.html',
    'search_advanced': 'bazhum/advanced_search.html',
    'search_results': 'bazhum/search_results.html',
    'journal': 'bazhum/czasopismo.html',
    'volume': 'bazhum/tom.html',
    'number': 'bazhum/numer.html',
    'article': 'bazhum/artykul.html',
    'main': 'bazhum/main_page.html',
    'about': 'bazhum/about.html',
    'social': 'bazhum/social.html',
    'export': 'bazhum/export.html',
    'journalList': 'bazhum/lista.html',
    }

media_prefix = '/static/bazhum/'
meta = {
    'scripts': {'jquery': media_prefix + '/scripts/jquery-1.7.2.min.js',
                'grid': media_prefix + 'scripts/gridPreview.js',
                'app': media_prefix + 'scripts/application.js',
				'lib': media_prefix + 'scripts/lib.js',
                'select': media_prefix + 'scripts/selection.js',
				'advsearch': media_prefix + 'scripts/advsearch.js', 
                'customSelect': media_prefix + 'scripts/jquery.customSelect.min.js',                 
                'orphanControl': media_prefix + 'scripts/jqwidont-compressed.js', 
                'ressearch': media_prefix + 'scripts/searchres.js'},
    'css':  {'style': media_prefix + 'styles/style.css'
            },
    'images': {'logo': media_prefix + 'images/logo_img_01.png',
                'logomhp': media_prefix + 'images/mhp_logo.jpg',
				'logotyp': media_prefix + 'images/bazhum_logo.png',},
    'title': 'BazHum',
    'export': {
            'Wybierz format': ['bibtex', 'selected="selected"'],
            'Bibtex': 'bibtex' ,
            'RIS': 'ris',
            },
    }
    
    
def exportTxt (qs, format):
    result = ''
    for obj in qs:
        if ArticleReview.objects.filter(par_id=obj.id).count() > 0:
            continue
        authors = []
        for auth in ArticleContributor.objects.filter(par_id=obj.id, role='author'):
            authors += [auth.title]
        authors = ', '.join([x for x in authors])
        if ArticleName.objects.filter(par_id=obj.id).count() > 0:
            title = (ArticleName.objects.filter(par_id=obj.id))[0]
        number = obj.sourceWithHier('number')
        yearName = ''
        volumeName = ''
        numberName = ''
        if number:
            numberName = number.getName
        volume = obj.sourceWithHier('volume')
        if volume:
            volumeName = volume.getName
        year = obj.sourceWithHier('year')
        if year:
            yearName = year.getName
        journal = obj.sourceWithHier('journal')
        pagesA = []
        for page in ArticlePages.objects.filter(par_id=obj.id):
            pagesA += [page]
        pages = 's.' + ','.join(map(unicode,pagesA))
        if format == 'bibtex':
            result += ''' @Article{%s, 
                     author = "%s",
                     title = "%s",
                     year =  %s,
                     volume =  %s,
                     number =  %s,
                     journal =  %s,
                     pages =  %s,
                    }\n '''  % (obj.id, authors, title.name_clean, yearName, volumeName, numberName, journal.__unicode__(), pages)
                    
        elif format == 'ris':
            pages = ''
            for p in pagesA:
                pages += 'SP - ' + p.page_from + '\n'
                pages += 'EP - ' + p.page_to + '\n'
            result += ''' 
TY  - JOUR 
AU - %s
TI - %s
PY - %s
VL - %s
NV - %s
JO - %s
%s ''' % (authors, authors, title.name_clean, yearName, volumeName, numberName, journal, pages)
                     
    return result
    
langDict = {
    'BG' : 'bułgarski',
    'CS' : 'czeski',
    'DE' : 'niemiecki',
    'EL' : 'grecki',
    'EN' : 'angielski',
    'ES' : 'hiszpański',
    'FR' : 'francuski',
    'HU' : 'węgierski',
    'IE' : 'occidental',
    'IT' : 'włoski',
    'LA' : 'łacina',
    'LN' : 'lingala',
    'LT' : 'litewski',
    'NL' : 'niderlandzki',
    'PA' : 'pendżabski',
    'PL' : 'polski',
    'PT' : 'portugalski',
    'RM' : 'retoromański',
    'RO' : 'rumuński',
    'RU' : 'rosyjski',
    'SA' : 'sanskryt',
    'SH' : 'serbsko-chorwacki',
    'SI' : 'syngaleski',
    'SK' : 'słowacki',
    'SO' : 'somalijski',
    'SR' : 'serbski',
    'SV' : 'szwedzki',
    'SW' : 'suahili',
    'UK' : 'ukraiński',
    }

def searchAdvanced(request):
    context = Context({	
			'templ': templates, 
			'meta': meta,
            'request': request,
			'extraJs': [meta['scripts']['advsearch']],
			"langs": sorted(langDict.items(), key=lambda x: x[1]),
		})
    return render_to_response(templates['search_advanced'], context)
    
def addObligMysql(str):
    result = []
    for w in str.split(' '):
        if w[1:] <> '-' and w <> 'OR':
            w = '+' + w
            result.append(w)
        else:
            result.append(w)
    
    OR_ids = [i for i, x in enumerate(result) if x == "OR"]
    for id in OR_ids:
        len = result.__len__()
        if id > 0:
            result[id-1] = re.sub('\+', '', result[id-1])
        if id < len-1:
            result[id+1] = re.sub('\+', '', result[id+1])
        result.pop(id)
    return ' '.join([x for x in result])
    # return str
    
def searchResults(request):
    deb = ''
    qs = Article.objects.all()
    # main query
    if 'generalQuery' in request.GET:
        queryStr = addObligMysql(request.GET['generalQuery'])
        qs = Article.objects.filter(articlename__name__search=queryStr).distinct()
        # jrls = JournalName.objects.filter(name__search=queryStr)
        # years = Year.objects.filter(journal_id__in=jrls.values_list('par_id'))
        # volumes = Volume.objects.filter(year_id__in=years)
        # if volumes.count() > 0:
            # numbers = Number.objects.filter(volume_id__in=volumes)
            # if numbers.count() > 0:
                # qs2 = qs.filter(number_id__in=numbers)
            # else:
                # qs2 = qs.filter(volume_id__in=volumes)
        # else:
            # numbers = Number.objects.filter(year_id__in=years)
            # qs2 = qs.filter(number_id__in=numbers) 
        # qs = qs | qs2
        
    # advanced query    
    elif 'typeField' in request.GET:
        if 'mode' in request.GET:
            mode = request.GET['mode']
        else:
            mode = 'all'

        addqs = Article.objects.none()
        
        valList = request.GET.getlist('valueField')
        
        for type in request.GET.getlist('typeField'):
            if type <> 'date':
                if valList[0] == '':
                    valList.pop(0)
                    continue
            if type == 'any':
                if mode == 'any':
                    addqs = addqs | qs.filter(articlename__name__search=addObligMysql(valList.pop(0)))
                else:
                    deb = addObligMysql(valList[0])
                    qs = qs.filter(articlename__name__search=addObligMysql(valList.pop(0)))
            elif type == 'title':
                if mode == 'any':
                    addqs = addqs | qs.filter(articlename__name_clean__search=addObligMysql(valList.pop(0)))
                else:
                    qs = qs.filter(articlename__name_clean__search=addObligMysql(valList.pop(0)))
            elif type == 'author':
                # authors = ArticleContributor.objects.filter(title__search=valList.pop(0))
                # qs = qs.filter(id__in=authors.values_list('par_id'))
                if mode == 'any':
                    addqs = addqs | qs.filter(articlecontributor__title__search=addObligMysql(valList.pop(0)))
                else:
                    qs = qs.filter(articlecontributor__title__search=addObligMysql(valList.pop(0)))
            elif type == 'jrl':
                jrls = JournalName.objects.filter(name__search=addObligMysql(valList.pop(0)))
                years = Year.objects.filter(journal_id__in=jrls.values_list('par_id'))
                volumes = Volume.objects.filter(year_id__in=years)
                if volumes.count() > 0:
                    numbers = Number.objects.filter(volume_id__in=volumes)
                    if numbers.count() > 0:
                        if mode == 'any':
                            addqs = addqs | qs.filter(number_id__in=numbers)
                        else:
                            qs = qs.filter(number_id__in=numbers)
                    else:
                        if mode == 'any':
                            addqs = addqs | qs.filter(volume_id__in=volumes)
                        else:
                            qs = qs.filter(volume_id__in=volumes)
                else:
                    numbers = Number.objects.filter(year_id__in=years)
                    if mode == 'any':
                        addqs = addqs | qs.filter(number_id__in=numbers) 
                    else:
                        qs = qs.filter(number_id__in=numbers) 
            elif type == 'date':
                yFrom = valList.pop(0)
                yTo = valList.pop(0)
                years = Year.objects.none()
                if yFrom <> '' and yTo <> '':
                    years = YearName.objects.filter(Q(name__gte=yFrom) & Q(name__lte=yTo))
                elif yFrom <> '' and yTo == '':
                    years = YearName.objects.filter(name__gte=yFrom)
                elif yFrom == '' and yTo <> '':
                    years = YearName.objects.filter(name__lte=yTo)
                    
                qs1 = Article.objects.none()
                volumes = Volume.objects.filter(year_id__in=years.values_list('par_id'))
                if volumes.count() > 0:
                    numbers = Number.objects.filter(volume_id__in=volumes)
                    if numbers.count() > 0:
                        qs1 = qs.filter(number_id__in=numbers)
                    else:
                        qs1 = qs.filter(volume_id__in=volumes)
                numbers = Number.objects.filter(year_id__in=years.values_list('par_id'))
                if numbers.count() > 0:
                    qs1 = qs1 | qs.filter(number_id__in=numbers) 
                if mode == 'any':
                    addqs = addqs | qs.filter(id__in=qs1.values_list('id'))
                else:
                    qs = qs.filter(id__in=qs1.values_list('id'))
            elif type == 'lang':
                if mode == 'any':
                    addqs = addqs.distinct() | qs.filter(articlename__lang=valList.pop(0)).distinct()
                else:
                    qs = qs.filter(articlename__lang=valList.pop(0)).distinct()
    
        if mode == 'any':
            qs = addqs
        
    # adjust filters
    if 'fa' in request.GET:
        for faInst in request.GET.getlist('fa'):
            qs = qs.filter(articlecontributor__title=(ArticleContributor.objects.get(id=faInst)).title)
    if 'fj' in request.GET:
        for fjInst in request.GET.getlist('fj'):
            years = Year.objects.filter(journal_id=fjInst)
            volumes = Volume.objects.filter(year_id__in=years)
            if volumes.count() > 0:
                numbers = Number.objects.filter(volume_id__in=volumes)
                if numbers.count() > 0:
                    qs = qs.filter(number_id__in=numbers)
                else:
                    qs = qs.filter(volume_id__in=volumes)
            else:
                numbers = Number.objects.filter(year_id__in=years)
                qs = qs.filter(number_id__in=numbers) 
    if 'fl' in request.GET:
        for flInst in request.GET.getlist('fl'):
            qs = qs.filter(articlename__lang=flInst).distinct()
    if 'fFrom' in request.GET:
        yFrom = request.GET['fFrom']
        yTo = request.GET['fTo']
        years = Year.objects.none()
        if yFrom <> '' and yTo <> '':
            years = YearName.objects.filter(Q(name__gte=yFrom) & Q(name__lte=yTo))
        elif yFrom <> '' and yTo == '':
            years = YearName.objects.filter(name__gte=yFrom)
        elif yFrom == '' and yTo <> '':
            years = YearName.objects.filter(name__lte=yTo)
           
        qs1 = Article.objects.none()
        volumes = Volume.objects.filter(year_id__in=years.values_list('par_id'))
        if volumes.count() > 0:
            numbers = Number.objects.filter(volume_id__in=volumes)
            if numbers.count() > 0:
                qs1 = qs.filter(number_id__in=numbers)
            else:
                qs1 = qs.filter(volume_id__in=volumes)
        numbers = Number.objects.filter(year_id__in=years.values_list('par_id'))
        if numbers.count() > 0:
            qs1 = qs1 | qs.filter(number_id__in=numbers) 
        
        qs = qs.filter(id__in=qs1.values_list('id'))
             
    results = []
    authorFilter = {}
    journalFilter = {}
    langFilter = {}
    
    for article in qs[:300]:
        # przygotowuje filtr jezykow
        if ArticleName.objects.filter(par_id=article.id).count() > 0:
            an = (ArticleName.objects.filter(par_id=article.id))[0]
            if an.lang in langFilter:
                langFilter[an.lang] += 1
            else:
                langFilter[an.lang] = 1
            
        # przygotowuje filtr czasopism
        if hasattr(article.sourceWithHier('journal'), 'id'):
            j = Journal.objects.get(id=article.sourceWithHier('journal').id)
            if j.id in journalFilter:
                journalFilter[j.id]['cnt'] += 1
            else:
                journalFilter[j.id] = {}
                journalFilter[j.id]['cnt'] = 1
                journalFilter[j.id]['name'] = j.getName
        
        # filtr autorów        
        for author in article.getAuthors:
            if author.id in authorFilter:
                authorFilter[author.title]['cnt'] += 1
            else:
                authorFilter[author.title] = {}
                authorFilter[author.title]['cnt'] = 1
                authorFilter[author.title]['title'] = author.title
                authorFilter[author.title]['id'] = author.id
                # authorFilter[author.id]['id'] = author.id
    
    for article in qs:
        # przygotowuje rekord
        fullArticle = {
                # 'id': article.id,
                'article': article,
                'pages': ArticlePages.objects.filter(par_id=article.id),
                'journal': article.sourceWithHier('journal'),
                'year': article.sourceWithHier('year'),
                'volume': article.sourceWithHier('volume'),
                'number': article.sourceWithHier('number'),                                
            }
        results += [fullArticle]
    
    authorFilter = sorted(authorFilter.iteritems(), key=lambda a: a[1], reverse=True)
    journalFilter = sorted(journalFilter.iteritems(), key=lambda a: a[1], reverse=True)
    langFilter = sorted(langFilter.iteritems(), key=lambda a: a[1], reverse=True)
        
    activeFilters = []
    
    for g in request.GET:
        if g == 'fj':
            for gv in request.GET.getlist(g):
                obj = Journal.objects.get(id=gv).getName
                if obj.__unicode__().__len__() > 60:
                    objName = obj.__unicode__()[:60] + '...'
                else:
                    objName = obj.__unicode__()
                activeFilters += [{
                    'name': 'Czasopismo', 
                    'id': gv, 
                    'obj': objName, 
                    'url': request.get_full_path().replace(g+'='+gv, '') }]
        elif g == 'fa':
            for gv in request.GET.getlist(g):
                obj = (ArticleContributor.objects.get(id=gv)).title
                if obj.__len__() > 60:
                    objName = obj[:60] + '...'
                else:
                    objName = obj
                activeFilters += [{
                    'name': 'Autor', 
                    'id': gv, 
                    'obj': objName, 
                    'url': request.get_full_path().replace(g+'='+gv, '') }]
        elif g == 'fl':
            for gv in request.GET.getlist(g):
                activeFilters += [{
                    'name': 'Język', 
                    'id': gv, 
                    'obj': gv, 
                    'url': request.get_full_path().replace(g+'='+gv, '') }]
        elif g == 'dateRange':
            valFrom = request.GET['fFrom']
            valTo = request.GET['fTo']
            activeFilters += [{
                'name': 'Rok wydania', 
                'id':  valFrom + '-' + valTo, 
                'obj': valFrom + '-' + valTo,
                'url': request.get_full_path().replace('fFrom='+valFrom, '').replace('fTo='+valTo, '').replace('dateRange=1','') }]
        
    context = Context({ 
            'deb': deb,
            'templ': templates, 
            'meta': meta,
            'qs': results,
            'extraJs': [meta['scripts']['ressearch'], meta['scripts']['select']],
            'request': request,
            'activeFilters': activeFilters,
            'filters': {
                    'filterJournal': journalFilter,
                    'filterAuthor': authorFilter,
                    'filterLang': langFilter,
                },
        })
    return render_to_response(templates['search_results'], context)
	
def servAjax(request):
	return ''
    
def numberNameConv(str):
    res = str
    if '-' in str:
        str = str.split('-')[0]
    elif '/' in str:
        str = str.split('/')[0]
    elif ' ' in str:
        str = str.split(' ')[0]
    try:
        res = int(re.sub('[^0-9]+', '', str))
    except ValueError:
        res = str
    return res
    
def yearNameConv(str):
    res = str.name
    str = str.name
    if '-' in str:
        str = str.split('-')[0]
    elif '/' in str:
        str = str.split('/')[0]
    elif ' ' in str:
        str = str.split(' ')[0]
    try:
        res = int(str)
    except ValueError:
        res = str
    return res
    
def showJournal(request, id):
    jrl = Journal.objects.get(id=id)
    years = sorted(Year.objects.filter(journal_id=jrl), key=lambda a: yearNameConv(a.getName), reverse=True)
    
    records = []
    for y in years:
        vol = Volume.objects.filter(year_id=y)
        numbers=Number.objects.filter(Q(volume_id=vol) | Q(year_id=y))
        numberNames = sorted(NumberName.objects.filter(par_id__in=numbers), key=lambda a: numberNameConv(a.name))
        sorted_ids = []
        prevItem = ''
        for x in numberNames:
            if prevItem == '':
                prevItem = x.par_id.id
                sorted_ids += [x.par_id.id]
            if x.par_id.id not in sorted_ids:
                sorted_ids += [x.par_id.id]
            
        rec = {'year': y,
            'volume': vol,
            'numbers': ({'nn': (NumberName.objects.filter(par_id=x))[0], 'id': x} for x in sorted_ids),}
        records += [rec]
    
    context = Context({	
            'jrl': jrl,
            'records': records,
			'templ': templates, 
			'meta': meta,
            'request': request,
			'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['journal'], context)
    
def showVolume(request, id):
    if Volume.objects.filter(id=id).count() > 0:
        volume = Volume.objects.get(id=id)
        year = volume.year_id
    else:
        year = Year.objects.get(id=id)
    
    numberNames = sorted(NumberName.objects.filter(par_id__in=Number.objects.filter(Q(volume_id=volume) | Q(year_id=year))), key=lambda a: numberNameConv(a.name), reverse=True)
    numbers = Number.objects.filter(Q(volume_id=volume) | Q(year_id=year))
    articles = Article.objects.filter(Q(number_id__in=numbers) | Q(volume_id=volume)).distinct()
    articles = articles.filter(~Q(id__in=ArticleReview.objects.values('par_id')))
    articlesDict = []
    for art in articles:
        articleNames = ArticleName.objects.filter(par_id=art.id)
        if articleNames.count() > 0:
            articleName = (ArticleName.objects.filter(par_id=art.id))[0]

        articlesDict += [{'id': art.id, 'name': articleName, 'authors': art.getAuthors}]
    context = Context({	
            'jrl': year.journal_id,
            'year': year,
            'volume': volume,
            'numbers': numbers,
            'numberNames': numberNames,
            'articles': sorted(articlesDict, key=lambda x: x['name'].name_clean),
			'templ': templates, 
			'meta': meta,
            'request': request,
			'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['volume'], context)
    
def showNumber(request, id):
    volume = None
    number = Number.objects.get(id=id)
    if number.volume_id:
        volume = Volume.objects.get(id=number.volume_id.id)
        year = volume.year_id
    else:
        year = number.year_id
    
    articles = Article.objects.filter(number_id=number).order_by('articlename__name')
    context = Context({	
            'jrl': year.journal_id,
            'year': year,
            'volume': volume,
            'number': number,
            'articles': articles,
			'templ': templates, 
			'meta': meta,
            'request': request,
			'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['number'], context)
    
def showArticle(request, id):
    number = []
    volume = []
    article = Article.objects.get(id=id)
    if article.number_id:
        number = Number.objects.get(id=article.number_id.id)
        if number.volume_id:
            volume = Volume.objects.get(id=number.volume_id.id)
            year = volume.year_id
        else:
            year = number.year_id
    else:  
        volume = article.volume_id
        year = volume.year_id

    if hasattr(year, 'journal_id'):
        journal = year.journal_id
    else:
        journal = ''
        
    reviews = ArticleReview.objects.filter(par_id=article)
        
    pages = ArticlePages.objects.filter(par_id=article)
    context = Context({	
            'jrl': journal,
            'year': year,
            'volume': volume,
            'number': number,
            'article': article,
            'reviews': reviews,
			'templ': templates, 
            'pages': pages,
			'meta': meta,
            'request': request,
            'zotero': 1,
			'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['article'], context)
    
def about(request):
    context = Context({	
			'templ': templates, 
			'meta': meta,
			# 'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['about'], context)
    
def journalList(request):
    alph = ['A','B','C','Ć','D','E','F','G','H','I','J','K','L','Ł','M','N','O','P','R','Q','S','Ś','T','U','V','W','X','Y','Z','Ź','Ż','#']
    records = {}
    records['#'] = []
    activeLetters = set()
    for j in Journal.objects.all():
        sanitize = re.sub(r'\W+', '', j.__unicode__())
        activeLetters.add(sanitize[:1].upper())
        if sanitize[:1].upper() in records:
            if sanitize[:1].upper().isdigit():
                records['#'] += [j]
            else:
                records[sanitize[:1].upper()] += [j]
        else:
            records[sanitize[:1].upper()] = [j]
    
    sortedRec = {}
    for key in sorted(records.iterkeys()):
         sortedRec[key] = sorted(records[key], key=lambda x: re.sub(r'\W+', '', x.getName.__unicode__()))
    context = Context({	
            'alph': alph,
            'records': sortedRec,
            'activeLetters': sorted(list(activeLetters)),
			'templ': templates, 
			'meta': meta,
            'request': request,
			# 'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['journalList'], context)
    
def main(request):
    context = Context({	
			'templ': templates, 
			'meta': meta,
			# 'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['main'], context)
    
def export(request):
    if request.GET['ids'] == "" and request.GET['idsSec'] == "":
        result = 'Musisz zaznaczyć obiekty do eksportu !'
        title = 'brak_zaznaczenia'
    elif request.GET['idsType'] == 'vol':
        title = 'Rocznik'
        volumes = []
        numbers = []
        if not 'y' in request.GET['ids']:
            volumes = Volume.objects.filter(id__in=request.GET['ids'].split(','))        
            numbers = Number.objects.filter(volume_id__in=volumes)
            title = volumes[0].year_id.__unicode__()
        else:
            numbers = Number.objects.filter(year_id__in=re.sub('y','',request.GET['ids']).split(','))
            title = numbers[0].year_id.__unicode__()
        articles = Article.objects.filter(Q(volume_id__in=volumes) | Q(number_id__in=numbers))
        result = exportTxt(articles, request.GET['type'])        
        # title = volumes[0].year_id.__unicode__()
    elif request.GET['idsType'] == 'num_art':
        artIds = []
        numbers = []
        title = 'tom'
        if request.GET['idsSec'] <> '':
            numbers = Number.objects.filter(id__in=request.GET['idsSec'].split(','))
            if numbers.count() > 0:
                title = numbers[0].volume_id.__unicode__()
        if request.GET['ids'] <> '':
            artIds = request.GET['ids'].split(',')
        articles = Article.objects.filter(Q(number_id__in=numbers) | Q(id__in=artIds))
        result = exportTxt(articles, request.GET['type'])
        if title == 'tom':
            title = articles[0].volume_id.__unicode__()

    else:
        artQs = Article.objects.filter(id__in=request.GET['ids'].split(','))
        result = exportTxt(artQs, request.GET['type'])
        title = artQs[0].__unicode__()
        
    title = re.sub('[^a-zA-Z0-9_]+', '', title.replace(' ', '_'))
    response = HttpResponse(result.replace('\n', '\r\n'), mimetype='text/plain;charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename='+title+'.txt'
    return response