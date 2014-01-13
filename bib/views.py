# -*- coding: utf-8 -*-

# OAI PMH support
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.flatpages.models import FlatPage
# from django_oaipmh import OAIProvider
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from django.template import Context, loader
from django.db.models import Q, Min, Count
from django.forms.models import modelform_factory
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from registration.models import * 
import re
import md5
from django.http import Http404

from bib.models import *
from bib.util import *
from bib.forms import *
from lib2to3.fixer_util import String

templates = {
    'header': 'bib/header.html',
    'footer': 'bib/footer.html',
    'search_advanced': 'bib/advanced_search.html',
    'search_results': 'bib/search_results.html',
    'search_results_mobile': 'bib/search_results_mobile.html',
    'journal': 'bib/czasopismo.html',
    'volume': 'bib/tom.html',
    'number': 'bib/numer.html',
    'article': 'bib/artykul.html',
    'main': 'bib/main_page.html',
    'about': 'bib/about.html',
    'social': 'bib/social.html',
    'export': 'bib/export.html',
    'journalList': 'bib/lista.html',
    'resultItem': 'bib/resultItem.html',
    'article_mod': 'bib/article_mod.html',
    'loginbox': 'bib/loginbox.html',
    'eshelf': 'bib/eshelf.html',
    'eshelf_link': 'bib/eshelf_link.html',
    'list_lib': 'bib/list_lib.html',
    'list_pub': 'bib/list_pub.html',
    'recordset': 'bib/recordset.html',
    'logout': 'bib/logout.html',
    'mesg': 'bib/mesg.html',
    'failedActivation': 'bib/failedActivation.html',
    'successActivation': 'bib/successActivation.html',    
    'passwordReset': 'bib/passwordReset.html',
    'passReset_email': 'bib/passReset_email.txt',
    'list_pub': 'bib/lista_wydawcy.html',
}

media_prefix = '/static/bazhum/'
meta = {
    'scripts': {'jquery': media_prefix + '/scripts/jquery-1.7.2.min.js',
                'grid': media_prefix + 'scripts/gridPreview.js',
                'app': media_prefix + 'scripts/application.js',
				'lib': media_prefix + 'scripts/lib.js',
                'select': media_prefix + 'scripts/selection.js',
                'article_mod': media_prefix + 'scripts/article_mod.js',
				'advsearch': media_prefix + 'scripts/advsearch.js',               
                'orphanControl': media_prefix + 'scripts/jqwidont-compressed.js',
                'eshelf': media_prefix + 'scripts/eshelf.js', 
                'jquery1103_ui': media_prefix + 'scripts/jquery-ui-1.10.3.custom.min.js',
                'jquery1103_ui_ac': media_prefix + 'scripts/jquery-ui-1.10.3.custom_ac.min.js',
                'jquery_validate': media_prefix + 'scripts/jquery.validate.js',
                'ressearch': media_prefix + 'scripts/searchres.js'},
    'css':  {'style': media_prefix + 'styles/style.css'
            },
    'images': {'logo': media_prefix + 'images/logo_img_01.png',
                'biglogo': media_prefix + 'images/big_logo_03.png',               
                'logomhp': media_prefix + 'images/mhp_logo.jpg',
                'rss': media_prefix + 'images/rss_icon_09.png',
				'logotyp': media_prefix + 'images/bazhum_logo.png',},
    'title': 'BazHum',
    'export': {
            _('Wybierz format'): ['bibtex', 'selected'],
            'Bibtex': 'bibtex' ,
            'RIS': 'ris',
            },
    'download': {
            'logo': media_prefix + 'images/bazhum_logo-01.jpg',
            'poster': media_prefix + 'images/BazHum_plakat_www_1.pdf',
            },
    'forms': {
            'registration': registrationForm,
            'login': loginForm,
            },
    }

def searchAdvanced(request):
    context = RequestContext(request, {	
			'templ': templates, 
            'ehself_count': eshelfCount(request),
			'meta': meta,
            'title': meta['title'] + ' - wyszukiwanie zaawansowane',
            'request': request,
			'extraJs': [meta['scripts']['advsearch']],
			"langs": Language.objects.all().order_by('lang'),
		})
    return render_to_response(templates['search_advanced'], context)
    
def searchResults(request):
    deb = ''
    qs = Dw.objects.all()
    
    qs = processQuery(qs, request)
             
    results = []
    
#     FILTER FROM DB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     authorFilter = ArticleContributor.objects \
#                         .filter(par_id__in=qs.values('id')) \
#                         .values('surname', 'firstname', 'title') \
#                         .annotate(Count('title')).order_by('-title__count')
#     journalFilter = qs.values('idjrl', 'journal').annotate(Count('idjrl')).order_by('-idjrl__count')
#     langFilter = qs.values('lang').annotate(Count('lang')).order_by('-lang__count')
    
    authorFilter = {}
    journalFilter = {}
    langFilter = {}
    
    qs = processQueryFilters(qs, request)
#     qs = qs.filter(accepted=True)

    idsToFilter = qs.values_list('id', flat=True)
    journalFilter = Dw.objects.filter(id__in=idsToFilter).values_list('idjrl', 'journal').annotate(Count('idjrl')).order_by('-idjrl__count')
    authorFilter = ArticleContributor.objects.filter(role='author', par_id__in=idsToFilter).values_list('title').annotate(Count('title')).order_by('-title__count')
    langFilter = Dw.objects.filter(id__in=idsToFilter).values_list('lang').annotate(Count('lang')).order_by('-lang__count')
    
#    DJANGO IN MEM FACETS
#     for dw in qs:
#         if not dw.idjrl_id in journalFilter:
#             journalFilter[dw.idjrl_id] = {'idjrl__count': 1, 'journal': dw.journal, 'idjrl': dw.idjrl_id }
#         else:
#             journalFilter[dw.idjrl_id]['idjrl__count'] += 1  
#         authors = dw.authors.split(',')
#          
#         for a in authors:
#             if a != '':
#                 if not a in authorFilter:
#                     authorFilter[a] = {'author': a, 'cnt': 1}
#                 else:
#                     authorFilter[a]['cnt'] += 1
#                  
#         if not dw.lang in langFilter:
#             langFilter[dw.lang] = {'lang': dw.lang, 'cnt': 1}
#         else:
#             langFilter[dw.lang]['cnt'] += 1
    
    getValues = []
    for key in request.GET.iterkeys(): 
        valuelist = request.GET.getlist(key)
        getValues += valuelist
    
    qs = processQueryPagination(qs)
    
#    DJANGO IN MEM FACETS
#     authorFilter = sorted(authorFilter.iteritems(), key=lambda a: a[1]['cnt'], reverse=True)
#     journalFilter = sorted(journalFilter.iteritems(), key=lambda a: a[1]['idjrl__count'], reverse=True)
#     langFilter = sorted(langFilter.iteritems(), key=lambda a: a[1]['cnt'], reverse=True)
        
    activeFilters = []
    activeFiltersVals = request.GET.getlist('fl') + request.GET.getlist('fj') + request.GET.getlist('fa') 
    
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
            import urllib2
            for gv in request.GET.getlist(g):
                if ArticleContributor.objects.filter(title=gv):
                    obj = (ArticleContributor.objects.filter(title=gv)[0]).getCustomTitle()                
                    if obj.__len__() > 60:
                        objName = obj[:60] + '...'
                    else:
                        objName = obj
                    activeFilters += [{
                        'name': 'Autor', 
                        'id': gv, 
                        'obj': objName, 
                        'url': request.get_full_path().replace(g+'='+ urllib2.quote(gv.encode('utf8')), '') }]
        elif g == 'fl':
            for gv in request.GET.getlist(g):
                activeFilters += [{
                    'name': 'Język', 
                    'id': gv, 
                    'obj': gv, 
                    'url': request.get_full_path().replace(g+'='+gv, '') }]
    if 'fFrom' in request.GET:
        valsFrom = request.GET.getlist('fFrom')
        valsTo = request.GET.getlist('fTo')
        for x in range(0, len(valsFrom)):
            activeFilters += [{
            'name': 'Rok wydania', 
            'id':  valsFrom[x] + '-' + valsTo[x], 
            'obj': valsFrom[x] + '-' + valsTo[x],
            'url': request.get_full_path().replace('&fFrom='+valsFrom[x]+'&fTo='+valsTo[x], '') }]
                
    
    context = RequestContext(request, { 
            'deb': deb,
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'] + ' - wyniki wyszukiwania',
            'qs': qs,
            'extraJs': [meta['scripts']['ressearch'], meta['scripts']['select']],
            'request': request,
            'activeFilters': activeFilters,
            'activeFiltersVals': activeFiltersVals,
            'filters': {
                    'filterJournal': journalFilter[:100],
                    'filterAuthor': authorFilter[:100],
                    'filterLang': langFilter[:100],
                },
        })
    return render_to_response(templates['search_results'], context)

def searchResultsMobile(request):
    deb = ''
    qs = Dw.objects.all()
    pageNo = request.GET.get('pageNo', 1)
    if not isinstance(pageNo, int):
        pageNo = 1
    qs = processQuery(qs, request)
    p = Paginator(qs, 15)
    page = p.page(pageNo)
    pages = []
    objPerPage = None
    
    if qs.exists():
        p = Paginator(qs, 15)
        pageNo = int(request.GET.get('pageNo', 1))
        currPage = p.page(pageNo)
        objPerPage = currPage.object_list
        
        if currPage.has_other_pages():
            if pageNo < 4:
                for i in range(7):
                    pages += [p.page(i+1)]
            elif pageNo > p.num_pages - 3:
                for i in range(p.num_pages-7, p.num_pages):
                    pages += [p.page(i+1)]
            else:
                for i in range(pageNo-3, pageNo+4):
                    pages += [p.page(i)]
                    
                    
    context = RequestContext(request, { 
            'deb': deb,
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'] + ' - wyniki wyszukiwania',
            'qs': objPerPage,
            'extraJs': [],
            'request': request,
#             PAGINATOR RELATED
            'pgn': p,
            'page': currPage,
            'pageList': pages,
            'pageNo': pageNo,
        })
    return render_to_response(templates['search_results_mobile'], context)
    
    
def servAjax(request):
    context = {}
    type = request.GET.get('type', '')

    if type == 'results':
        pageNo = request.GET.get('pageNo', '')
        qs = Dw.objects.all()
        qs = processQuery(qs, request)
        qs = processQueryFilters(qs, request)
        qs = processQueryPagination(qs, pagination={'from': (int(pageNo)-1)*20, 'to': int(pageNo)*20})
#         results = prepareResultRecord(qs)
        context = RequestContext(request, {'qs': qs})
        if not qs:
            return HttpResponse('')
        return render_to_response(templates['resultItem'], context)
    elif type == 'eshelf_add':
        if request.user.is_authenticated:
            resDict = parsSelUrl(request)
            articles = resDict['articles']
            if not isinstance(articles, basestring)  :        
                for art in articles:
                    dwObj = Dw.objects.get(id=art.pk)
#                     if dwObj.accepted:
                    Eshelf.objects.filter(user=request.user.id, article=art).delete()
                    usr = User.objects.get(id=request.user.id)
                    record = Eshelf(user=usr, article=art)
                    record.save()
            return HttpResponse(eshelfCount(request))
    elif type == 'folder_add':
        if request.user.is_authenticated:
            folder = FolderHierarchy(name=request.GET.get('name', 'bez nazwy'), user=request.user)
            folder.save()
            return HttpResponse(folder.id)
    elif type == 'folder_rename':
        if request.user.is_authenticated:
            folder = FolderHierarchy.objects.get(id=request.GET['id'])
            folder.name = request.GET.get('name', 'bez nazwy')
            folder.save()
            return HttpResponse(folder.name)
    elif type == 'folder_empty':
        if request.user.is_authenticated:
            folderId = None
            if request.GET['id'] != '0':
                folderId = request.GET['id']
            Eshelf.objects.filter(parent_id=folderId).delete()
            return HttpResponse('ok')
    elif type == 'folder_del':
        if request.user.is_authenticated:
            Eshelf.objects.filter(parent__in=FolderHierarchy.objects.filter(id=request.GET.get('id',0))).delete()
            FolderHierarchy.objects.filter(id=request.GET.get('id',0)).delete()
            return HttpResponse('usuniety')
    elif type == 'article_move':
        if request.user.is_authenticated:
            Eshelf.objects.filter(user=request.user, article__id=request.GET['idArt']).update(parent=request.GET['idDir'])
            return HttpResponse(request.GET['idArt'])
    elif type == 'article_del':
        if request.user.is_authenticated:
            Eshelf.objects.filter(user=request.user, article__id=request.GET['idArt']).delete()
            return HttpResponse(request.GET['idArt'])
    return HttpResponse('')
    
def showJournal(request, id):
    jrl = Journal.objects.get(id=id)
    
    records2 = []
    showAccepted = (Q(accepted=True) | Q(accepted=False) | Q(accepted=None))
#    if request.user.groups.filter(name='pub').count() > 0:
#        showAccepted = Q(Q(accepted=True) | Q(accepted=False))
    
    dwQs = Dw.objects.filter(Q(idjrl=id) & showAccepted) \
                .values_list('idyear', 'year', 'idvol', 'volume', 'idno', 'number').distinct().order_by('idyear', 'year', 'volume', 'number')
    
    first = True
    idyear = ''
    year = ''
    idvol = ''
    volume = ''
    idno = ''
    numbers = []
    acceptedVol = ''
    acceptedNo = ''
    
    if len(dwQs) != 1:
        for r in dwQs:
            acceptedVol = ''
            acceptedNo = ''
            if first:
                idyear = r[0]
                year = r[1]
                idvol = r[2]
                if Volume.objects.filter(id=idvol).exists() and request.user.is_authenticated():
                    acceptedVol = Volume.objects.get(id=idvol).isAccepted
                volume = unicode(r[3]) + acceptedVol 
                first = False
                numbers = []
            if r[2] != idvol:
                numbers = sorted(numbers, key=lambda x: numberNameConv(x[1]))
                records2 += [(idyear, year, idvol, volume, numbers)]
                idyear = r[0]
                year = r[1]
                idvol = r[2]
                if Volume.objects.filter(id=idvol).exists() and request.user.is_authenticated():
                    acceptedVol = Volume.objects.get(id=idvol).isAccepted
                volume = unicode(r[3]) + acceptedVol
                if r[5] != '' and r[5] != None and r[4] != '':                    
                    if Number.objects.filter(id=r[4]).exists() and request.user.is_authenticated():
                        acceptedNo = Number.objects.get(id=r[4]).isAccepted
                    numbers = [(r[4], unicode(r[5]) + acceptedNo)]
                else:
                    numbers = []
            elif r[0] != idyear:
                numbers = sorted(numbers, key=lambda x: numberNameConv(x[1]))
                records2 += [(idyear, year, idvol, volume, numbers)]
                idyear = r[0]
                year = r[1]
                idvol = r[2]
                if Volume.objects.filter(id=idvol).exists() and request.user.is_authenticated():
                    acceptedVol = Volume.objects.get(id=idvol).isAccepted
                volume = unicode(r[3]) + acceptedVol
                if r[5] != '' and r[5] != None and r[4] != '':
                    if Number.objects.filter(id=r[4]).exists() and request.user.is_authenticated():
                        acceptedNo = Number.objects.get(id=r[4]).isAccepted
                    numbers = [(r[4], unicode(r[5]) + acceptedNo)]
                else:
                    numbers = []
            else:
                if r[5] != '' and r[5] != None and r[4] != '':
                    if Number.objects.filter(id=r[4]).exists() and request.user.is_authenticated():
                        acceptedNo = Number.objects.get(id=r[4]).isAccepted
                    numbers += [(r[4], unicode(r[5]) + acceptedNo)]
    else:        
        idyear = dwQs[0][0]
        year = dwQs[0][1]
        idvol = dwQs[0][2]
        if Volume.objects.filter(id=idvol).exists() and request.user.is_authenticated():
            acceptedVol = Volume.objects.get(id=idvol).isAccepted
        volume = unicode(dwQs[0][3]) + acceptedVol
        numbers = []
        if dwQs[0][5] != '' and dwQs[0][5] != None and dwQs[0][4] != '': 
            if Number.objects.filter(id=dwQs[0][4]).exists() and request.user.is_authenticated():
                acceptedNo = Number.objects.get(id=dwQs[0][4]).isAccepted

            numbers = [dwQs[0][4], unicode(dwQs[0][5]) + acceptedNo]
        records2 += [(idyear, year, idvol, volume, numbers)]
    
    if records2[:1] != [(idyear, year, idvol, volume, numbers)]:
        records2 += [(idyear, year, idvol, volume, numbers)]
    records2 = sorted(records2, key=lambda x: (yearNameConv(x[1]), x[3]), reverse=True)    
    
    socialShare = jrl.__unicode__()
     
    context = RequestContext(request, {	
            'jrl': jrl,
            'jrlPerms': getJrlPerms(request),
            'records': records2,
#             'records': dwQs,
			'templ': templates, 
            'ehself_count': eshelfCount(request),
			'meta': meta,
            'title': meta['title'] + ' - ' + jrl.__unicode__(),
            'request': request,
			'extraJs': [meta['scripts']['select']],
            'socialShare': socialShare,
		})
    if in_admin_group(request.user):
        context['stats'] = Dw.objects.filter(Q(idjrl=id) & showAccepted).count()
        context['statsYrs'] = Dw.objects.filter(Q(idjrl=id) & showAccepted).values_list('idyear').distinct().count()
        context['statsVols'] = Dw.objects.filter(Q(idjrl=id) & showAccepted).values_list('idvol').distinct().count()
        context['statsNos'] = Dw.objects.filter(Q(idjrl=id) & showAccepted).values_list('idno').distinct().count()
        
    return render_to_response(templates['journal'], context)
    
def showVolume(request, id):
    if Volume.objects.filter(id=id).count() > 0:
        volume = Volume.objects.get(id=id)
        year = volume.year_id
        socialShare = volume.__unicode__()
    else:
        year = Year.objects.get(id=id)
        socialShare = year.__unicode__()
#     
#     numberNames = sorted(NumberName.objects.filter(par_id__in=Number.objects.filter(Q(volume_id=volume) | Q(year_id=year))), key=lambda a: numberNameConv(a.name), reverse=True)
#     numbers = Number.objects.filter(Q(volume_id=volume) | Q(year_id=year))
#     articles = Article.objects.filter(Q(number_id__in=numbers) | Q(volume_id=volume)).distinct()
#     articles = articles.filter(~Q(id__in=ArticleReview.objects.values('par_id')))
#     articlesDict = []
#     for art in articles:
#         articleNames = ArticleName.objects.filter(par_id=art.id)
#         if articleNames.count() > 0:
#             articleName = (ArticleName.objects.filter(par_id=art.id))[0]
#         
#         pages = ArticlePages.objects.filter(par_id=art.id)
#         pageFrom = 0
#         if pages.count() > 0:
#             pageFrom = pages[0].page_from
#         articlesDict += [{'id': art.id, 'name': articleName, 'authors': art.getAuthors, 'pageFrom': pageFrom}]
    showAccepted = Q(accepted=True) | Q(accepted=False) | Q(accepted=None)
#    if request.user.groups.filter(name='pub').count() > 0:
#        showAccepted = Q(Q(accepted=True) | Q(accepted=False))
    articles = Dw.objects.filter(Q(idvol=id) & showAccepted).order_by('-number', 'from_field')
    articles = sorted(articles, key=lambda a: (numberNameConv(a.number), a.from_field))
    context = RequestContext(request, {	
            'jrl': year.journal_id,
            'jrlPerms': getJrlPerms(request),
            'year': year,
            'volume': volume,
#             'numbers': numbers,
#             'numberNames': numberNames,
            'articles': articles,
			'templ': templates, 
            'ehself_count': eshelfCount(request),
			'meta': meta,
            'title': meta['title'] + ' - ' + volume.__unicode__(),
            'request': request,
			'extraJs': [meta['scripts']['select']],
            "socialShare": socialShare,
		})
    if in_admin_group(request.user):
        context['stats'] = len(articles)
    return render_to_response(templates['volume'], context)
    
def showNumber(request, id):
    volume = None
    number = Number.objects.get(id=id)
    if number.volume_id:
        volume = Volume.objects.get(id=number.volume_id.id)
        year = volume.year_id
    else:
        year = number.year_id
    
#     articles = Article.objects.filter(number_id=number).order_by('articlepages__page_from')
    showAccepted = Q(accepted=True) | Q(accepted=False) | Q(accepted=None)
#    if request.user.groups.filter(name='pub').count() > 0:
#        showAccepted = Q(Q(accepted=True) | Q(accepted=False))
    articles = Dw.objects.filter(Q(idno=id) & showAccepted).order_by('from_field')
    socialShare = number.__unicode__()
    context = RequestContext(request, {	
            'jrl': year.journal_id,
            'jrlPerms': getJrlPerms(request),
            'year': year,
            'volume': volume,
            'number': number,
            'articles': articles,
			'templ': templates, 
            'ehself_count': eshelfCount(request),
			'meta': meta,
            'title': meta['title'] + ' - ' + number.__unicode__(),
            'request': request,
			'extraJs': [meta['scripts']['select']],
            'socialShare': socialShare,
		})
    if in_admin_group(request.user):
        context['stats'] = len(articles)
    return render_to_response(templates['number'], context)
    
def showArticle(request, id):
    if request.GET:
        if in_admin_group(request.user):
            if 'accept_next' in request.GET:
                Dw.objects.filter(id=id).update(accepted=1)
                dwObj = Dw.objects.get(id=id)
                mappedJrl = Journalmap.objects.filter(iduser=request.user)            
                if Dw.objects.filter(idjrl__in=mappedJrl.values('idjrl'), accepted=False, idno=dwObj.idno) and dwObj.idno:
                    art = Dw.objects.filter(idjrl__in=mappedJrl.values('idjrl'), accepted=False, idno=dwObj.idno)[0]
                    return HttpResponseRedirect(reverse('bib.views.showArticle', args=(art.id,)))
                elif Dw.objects.filter(idjrl__in=mappedJrl.values('idjrl'), accepted=False, idvol=dwObj.idvol) and dwObj.idvol:
                    art = Dw.objects.filter(idjrl__in=mappedJrl.values('idjrl'), accepted=False, idvol=dwObj.idvol)[0]
                    return HttpResponseRedirect(reverse('bib.views.showArticle', args=(art.id,)))
                else:
                    return HttpResponseRedirect(reverse('bib.views.showJournal', args=(dwObj.idjrl_id,)))
    #             elif Dw.objects.filter(idjrl__in=mappedJrl.values('idjrl'), accepted=False):
    #                 art = Dw.objects.filter(idjrl__in=mappedJrl.values('idjrl'), accepted=False)[0]
    #                 return HttpResponseRedirect(reverse('bib.views.showArticle', args=(art.id,)))
    #             others = Dw.objects.filter(idjrl__in=jrls, accepted=False)
    #             if others:
    #                 id = others[1].id
    #                 return HttpResponseRedirect(reverse('bib.views.showArticle', args=(id,)))
            if 'del_art' in request.GET:
                
                rec = Dw.objects.get(id=id)
                vol = rec.idvol
                no = rec.idno
                Article.objects.get(id=rec.id).delete()
                rec.delete()
                if vol:
                    return HttpResponseRedirect(reverse('bib.views.showVolume', args=(vol.id,)))
                elif no:
                    return HttpResponseRedirect(reverse('bib.views.showNumber', args=(no.id,)))
            if 'edit' in request.GET:
                return HttpResponseRedirect(reverse('bib.views.article_mod', args=(id,)))
    number = []
    volume = []
    socialShare = ''
    article = None
    if Article.objects.filter(id=id).exists():
        article = Article.objects.get(id=id)
    else:
        raise Http404
        
    if article.number_id:
        number = Number.objects.get(id=article.number_id.id)
        socialShare += number.__unicode__() + ", "
        if number.volume_id:
            volume = Volume.objects.get(id=number.volume_id.id)
            year = volume.year_id
        else:
            year = number.year_id
    else:  
        volume = article.volume_id
        year = volume.year_id
        socialShare += volume.__unicode__() + ", "

    if hasattr(year, 'journal_id'):
        journal = year.journal_id
    else:
        journal = ''
        
    reviews = ArticleReview.objects.filter(par_id=article)
        
#     pages = ArticlePages.objects.filter(par_id=article)
    pages = article.getPages
    socialShare += article.__unicode__()
    context = RequestContext(request,{	
            'jrl': journal,
            'jrlPerms': getJrlPerms(request),
            'year': year,
            'volume': volume,
            'number': number,
            'article': article,
            'reviews': reviews,
			'templ': templates, 
            'ehself_count': eshelfCount(request),
            'pages': pages,
			'meta': meta,
            'title': meta['title'] + ' - ' + article.__unicode__(),
            'request': request,
            'zotero': 1,
			'extraJs': [meta['scripts']['select']],
            'cacheOff': True,
            'socialShare': socialShare,
            'acceptFlag': in_pub_group(request.user) and not Dw.objects.get(id=article.id).accepted,
		})
    return render_to_response(templates['article'], context)
    
def about(request):
    context = RequestContext(request,{	
			'templ': templates, 
            'ehself_count': eshelfCount(request),
			'meta': meta,
            'title': meta['title'] + ' - o projekcie',
			# 'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['about'], context)
    
def journalList(request):
    alph = ['A','B','C','Ć','D','E','F','G','H','I','J','K','L','Ł','M','N','O','P','Q','R','S','Ś','T','U','V','W','X','Y','Z','Ź','Ż','#']
    records = {}
    records['#'] = []
    activeLetters = set()
    
    for j in JournalName.objects.all():
#         sanitize = re.sub(r'\W+', '', j.__unicode__())
        sanitize = j.name.replace('The ', '')
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
#          sortedRec[key] = sorted(records[key], key=lambda x: re.sub(r'\W+', '', x.getName.__unicode__()))
        sortedRec[key] = sorted(records[key], key=lambda x: x.name)
    context = RequestContext(request,{	
            'alph': alph,
            'records': sortedRec,
            'activeLetters': sorted(list(activeLetters)),
			'templ': templates, 
            'ehself_count': eshelfCount(request),
			'meta': meta,
            'title': meta['title'] + ' - lista czasopism',
            'request': request,
			# 'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['journalList'], context)
    
def main(request):
    context = RequestContext(request, {	
			'templ': templates, 
            'ehself_count': eshelfCount(request),
			'meta': meta,
            'title': meta['title'],
            'request': request,
			# 'extraJs': [meta['scripts']['select']],
		})
    return render_to_response(templates['main'], context)
    
def export(request):
    resDict = parsSelUrl(request)
    result = exportTxt(resDict['articles'], request.GET['type'])    
    title = re.sub('[^a-zA-Z0-9_]+', '', resDict['title'].replace(' ', '_'))
    response = HttpResponse(result.replace('\n', '\r\n'), mimetype='text/plain;charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename='+title+'.txt'
    return response

def loginView(request):
    if 'username' not in request.POST:
        return HttpResponseRedirect(reverse('bib.views.main'))
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            mesg = _(u'Pomyślnie zalogowałeś się do systemu')
        else:
            mesg = u'Twoje konto jest zablokowane.'
    else:
        mesg = u'Podany adres nie jest zarejestrowany w naszej bazie :('
    
    context = RequestContext(request, {    
            'templ': templates, 
            'mesg': mesg,
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'],
            'request': request,
            # 'extraJs': [meta['scripts']['select']],
        })
    return render_to_response(templates['mesg'], context)

def registerView(request):
    form = None
    mesg = ''
    if request.POST:
        rForm = registrationForm(request.POST)
        if rForm.is_valid:
             errorsInUser = re.findall(r'[^a-zA-Z._-]', rForm['username'].value())
             if len(errorsInUser) > 0:
                 mesg = u'Podałeś niepoprawne dane w formularzu'
                 form = rForm
             else:
                 try:
                    from django.contrib.sites.models import get_current_site
                    registeredUser = RegistrationProfile.objects.create_inactive_user(rForm['username'].value(), 
                                                                                  rForm['email'].value(), 
                                                                                  rForm['password'].value(), 
                                                                                  get_current_site(request), 
                                                                                  True)
                    mesg = u'Na podany adres został wysłany e-mail z kodem aktywacyjnym.';
                 except:
                    mesg = u'Wystąpił błąd w trakcie rejestracji.';
            
        else:
            mesg = u'Podałeś niepoprawne dane w formularzu'
            form = rForm
    
    context = RequestContext(request, {    
            'templ': templates, 
            'mesg': mesg,
            'form': form,
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'],
            'request': request,
            # 'extraJs': [meta['scripts']['select']],
        })
    return render_to_response(templates['mesg'], context)

def logoutView(request):
    logout(request)
    context = RequestContext(request, {    
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'],
            'request': request,
            # 'extraJs': [meta['scripts']['select']],
        })
    return render_to_response(templates['logout'], context)

def activate(request, key):
    context = RequestContext(request, {    
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'],
            'request': request,
            # 'extraJs': [meta['scripts']['select']],
        })
    if not RegistrationProfile.objects.activate_user(key):
        return render_to_response(templates['failedActivation'], context)
    else:
        return render_to_response(templates['successActivation'], context)
    

@login_required
def e_shelf(request, dirid=0, pageFromUrl=1):
    pageNo = int(pageFromUrl)
    pages = []
    objPerPage = []    
    currPage = None
    
    folders = FolderHierarchy.objects.filter(user=request.user)
    records = Eshelf.objects.none()
    if int(dirid) == 0:
        records = Eshelf.objects.filter(user=request.user, parent__isnull=True)
    else:
        records = Eshelf.objects.filter(user=request.user, parent__id=dirid)
    articlesIds = list(records.values_list('article', flat=True))
    qs = Dw.objects.filter(id__in=articlesIds)
#     records = Eshelf.objects.filter(user=request.user, parent__isnull=True)
#     p = Paginator(qs, 15)
    p = None
    
    if qs.exists():
        p = Paginator(qs, 15)
        pageNo = int(pageFromUrl)
        page = p.page(pageNo)        
        currPage = p.page(pageNo)
        objPerPage = currPage.object_list
        
        if currPage.has_other_pages():
            pages = []
            if pageNo < 4:
                for i in range(7):
                    if (i+1) <= p.num_pages:
                        pages += [p.page(i+1)]
            elif pageNo > p.num_pages - 3:
                for i in range(p.num_pages-7, p.num_pages):
                    if (i+1) < p.num_pages:
                        pages += [p.page(i+1)]
            else:
                for i in range(pageNo-3, pageNo+4):
                    if i < p.num_pages:
                        pages += [p.page(i)]                
    
    context = RequestContext(request, {     
            'rootCnt': Eshelf.objects.filter(user=request.user, parent__isnull=True).count(),
            'templ': templates, 
            'folders': folders,
            'activeDir': dirid,
            'articles': objPerPage,
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'request': request,
            'title': meta['title']  + u' - Panel wydawcy',
            # PAGINATOR RELATED
            'pgn': p,
            'page': currPage,
            'pageList': pages,
            'pageNo': pageNo,
            'extraJs': [meta['scripts']['eshelf'], meta['scripts']['select'], meta['scripts']['jquery1103_ui']],
        })
    return render_to_response(templates['eshelf'], context)

@user_passes_test(in_pub_group, login_url='bib.views.main')
def list_publisher(request):
    jrls = Journal.objects.filter(id__in=Journalmap.objects.filter(iduser=request.user).values_list('idjrl', flat=True))
    context = RequestContext(request, {   
            'jrls': jrls,     
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'request': request,
            'title': meta['title']  + u' - Panel wydawcy',
            'extraJs': [meta['scripts']['select']],
        })
    return render_to_response(templates['list_pub'], context)    

@user_passes_test(in_lib_group, login_url='bib.views.main')
def list_librarian(request):
    if request.GET:
        ids = request.GET.getlist('checkbox')
        Dw.objects.filter(id__in=ids).update(accepted=True)
    jrls = Journal.objects.filter(id__in=Journalmap.objects.filter(iduser=request.user).values_list('idjrl', flat=True))
#     articlesIds = Dw.objects.filter(idjrl__in=jrls, accepted=False).values_list('id', flat=True).distinct()
#     articles = Article.objects.filter(id__in=articlesIds)
    context = RequestContext(request, {   
            'articles': Dw.objects.filter(idjrl__in=jrls, accepted=False),
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'request': request,
            'title': meta['title']  + u' - Panel wydawcy',
            'extraJs': [meta['scripts']['select']],
        })
    return render_to_response(templates['list_lib'], context)

@user_passes_test(in_lib_group, login_url='bib.views.main')
def article_mod(request, id=-1):    
    jrls = Journal.objects.filter(id__in=Journalmap.objects.filter(iduser=request.user).values('idjrl'))
    backToUrl = request.META['HTTP_REFERER'].split('?')[0]
    if request.POST:
        backToUrl = request.POST['backToUrl']
    context = RequestContext(request, {    
            'id': id,
            'form': None,
            'jrls': jrls,
            'langs': Language.objects.all(), 
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'request': request,
            'extraJs': [meta['scripts']['article_mod'], meta['scripts']['jquery1103_ui_ac']],
            'title': meta['title']  + u' - modyfikacja artykułu',
            'backToUrl': backToUrl,
            'formData': None,
            'cacheOFf': True,
            # 'extraJs': [meta['scripts']['select']],
        })
    
    if request.POST:
        errors = {}
        validate = {}
        
        postYear = request.POST.get('year', '')
        postVol = request.POST.get('volume', '')
        postNo = request.POST.get('number', '')
        
        
        validate['jrl'] = Journal.objects.get(id=request.POST['jrl'])
        if len(postYear) < 255:
            validate['year'] = postYear
        else:
            errors['year'] = 'Za długa wartość pola rok.'
            
        if len(postYear) != 0:
            validate['year'] = postYear
        else:
            errors['year'] = 'Wartość pola rok nie może być pusta.'
            
        
        if len(postVol) < 255:
            validate['vol'] = postVol
        else:
            errors['vol'] = 'Za długa wartość pola tom.'
            
        if len(postNo) < 255:
            validate['no'] = postNo
        else:
            errors['no'] = 'Za długa wartość pola numer.' 
        
        if postNo == '' and postVol == '':
            errors['vol_no'] = 'Musisz uzupełnić wartość pola numer lub tom.' 
        
        validate['titles'] = [] 
        errors['titles'] = []
        titlesCount = len(request.POST.getlist('titles-counter'))
#         context['debug'] = request.POST.getlist('titles-counter')
        for gt in range(0,titlesCount):
            
            titleRec = {}
            errRec = {}
                    
            gtUni = unicode(gt)
                    
            keyId = 'title-id-' + gtUni
            keyParId = 'title-par_id-' + gtUni
            keyTitle = 'title-' + gtUni
            keyLang = 'lang-' + gtUni
            postTitle = request.POST.get(keyTitle, '')
            postLang = request.POST.get(keyLang, '')                        
             
            if postTitle == '':
                continue
             
            if len(postTitle) < 1500:
                titleRec['title'] = postTitle
            else:
                errRec[keyTitle] = ['Za długa wartość pola tytuł, pozycja: ' + gtUni]
                
            if len(postLang) < 10:
                titleRec['lang'] = postLang
            else:
                errRec[keyLang] = ['Za długa wartość pola język tytułu, pozycja: ' + gtUni]
                
            if not errRec:
                validate['titles'] += [{
                             'id': request.POST.get(keyId, ''),
                             'par_id': request.POST.get(keyParId,''),
                             'name': titleRec['title'], 
                             'lang': titleRec['lang']}]
            else:
                errors['titles-'+gtUni] += [errRec]
        if errors['titles'] == []:
            errors.pop('titles', None)
        if len(validate['titles']) == 0:
            errors['titles_no'] = 'Musisz podać conajmniej jeden tytuł dla artykułu'
                
        validate['authors'] = []
        errors['authors'] = []
        authCount = len(request.POST.getlist('auth-counter'))  
        for ga in range(0,authCount):
            titleRec = {}
            errRec = {}
            
            gaUni = unicode(ga)
            
            keyId = 'auth-id-' + gaUni
            keyParId = 'auth-par_id-' + gaUni 
            keyFname = 'fname-' + gaUni
            keyLname = 'lname-' + gaUni
            keyType = 'AuthorType-' + gaUni
            postFirst = request.POST.get(keyFname,'') 
            postLast = request.POST.get(keyLname,'')
            postType = request.POST.get(keyType,'')
            
            if postFirst == '' and postLast == '':
                continue
            
            if len(postFirst) < 512:
                titleRec['fname'] = postFirst
            else:
                errRec[keyFname] = ['Za długa wartość pola imię autora, pozycja: ' + gaUni]
                
            if len(postLast) < 512:
                titleRec['lname'] = postLast
            else:
                errRec[keyLname] = ['Za długa wartość pola nazwisko autora, pozycja: ' + gaUni]
                
            if len(postType) < 255:
                titleRec['AuthorType'] = postType
            else:
                errRec[keyType] = ['Za długa wartość pola typ autora, pozycja: ' + gaUni]
        
            if not errRec:
                validate['authors'] += [{
                             'id': request.POST.get(keyId, ''),
                             'par_id': request.POST.get(keyParId, ''),
                             'firstname': titleRec['fname'], 
                             'surname': titleRec['lname'],
                             'role': titleRec['AuthorType']}]
            else:
                errors['authors'] += [errRec]
        if errors['authors'] == []:
            errors.pop('authors', None)        
        
        validate['pages'] = []
        errors['pages'] = {} 
        pagesCount = len(request.POST.getlist('pages-counter'))
        for gp in range(0,pagesCount):
            titleRec = {}
            errRec = {}
            
            gpUni = unicode(gp)
            
            keyId = 'page-id-' + gpUni
            keyParId = 'page-par_id-' + gpUni
            keyPageFrom = 'pFrom-' + gpUni
            keyPageTo = 'pTo-' + gpUni
            fieldPageFrom = request.POST.get(keyPageFrom, '')
            fieldPageTo = request.POST.get(keyPageTo, '') 
            
            if fieldPageFrom == '' and fieldPageTo == '':
                continue
            
            if len(fieldPageFrom) < 255:
                titleRec['pFrom'] = fieldPageFrom
            else:
                errRec['pFrom'] = 'Za długa wartość pola strona od'
                
            if re.match(r'^[0-9]+$', fieldPageFrom):
                titleRec['pFrom'] = fieldPageFrom
            else:
                errRec['pFrom'] = 'Wartość pola strona od musi być liczbą'
            
            if len(fieldPageTo) < 255:
                titleRec['pTo'] = fieldPageTo
            else:
                errRec['pTo'] = 'Za długa wartość pola strona do'
            
            if fieldPageTo != '':
                if re.match(r'^[0-9]+$', fieldPageTo):
                    titleRec['pTo'] = fieldPageTo
                else:
                    errRec['pTo'] = 'Wartość pola strona do musi być liczbą'
                
            
            validate['pages'] += [{
                         'id': request.POST.get(keyId, ''),
                         'par_id': request.POST.get(keyParId, ''),
                         'page_from': titleRec['pFrom'], 
                         'page_to': titleRec['pTo'], 
                         'errors': errRec}]
            if errRec:
                errors['pages'] = errRec
        if errors['pages'] == {}:
            errors.pop('pages', None)
        
        if errors:                
            context['formData'] = validate
            context['errData'] = errors
        else:            
            saveYear = None
            saveYearName = YearName.objects.filter(name=validate['year'], par_id__journal_id=validate['jrl'])
            if saveYearName:
                saveYearName = saveYearName[0]
            else:
                saveYear = Year(journal_id=validate['jrl'])
                if saveYear:
                    saveYear.save()
                saveYearName = YearName(par_id=saveYear, name=validate['year'])                    
                saveYearName.save()
                
            saveVolume = None
            saveVolumeName = VolumeName.objects.filter(name=validate['vol'], par_id__year_id=saveYearName.par_id)
            if saveVolumeName:
                saveVolumeName = saveVolumeName[0]
            else:
                if validate['vol'] != '':
                    saveVolume = Volume(year_id=saveYearName.par_id)
                    if saveVolume:
                        saveVolume.save()
                    saveVolumeName = VolumeName(par_id=saveVolume, name=validate['vol'])
                    saveVolumeName.save()
            
            saveNumber = None
            if saveVolumeName:
                saveNumberName = NumberName.objects.filter(name=validate['no'], par_id__volume_id=saveVolumeName.par_id)
            else:
                saveNumberName = NumberName.objects.filter(name=validate['no'], par_id__year_id=saveYearName.par_id)
            if saveNumberName:
                saveNumberName = saveNumberName[0]
            else:
                if validate['no'] != '':
                    if saveVolumeName:
                        saveNumber = Number(volume_id=saveVolumeName.par_id)
                    else:
                        saveNumber = Number(year_id=saveYearName.par_id)
                    if saveNumber:
                        saveNumber.save()
                    saveNumberName = NumberName(par_id=saveNumber, name=validate['no'])                        
                    saveNumberName.save()
            
            if id == -1:
                saveArticle = None
                authorStr = ''
                if saveNumberName:
                    saveArticle = Article(number_id=saveNumberName.par_id)
                else:
                    saveArticle = Article(volume_id=saveVolumeName.par_id)
                saveArticle.save()
                
                firstTitle = True
                for title in validate['titles']:
                    if firstTitle:
                        saveArticleName = ArticleName(par_id = saveArticle,
                                                      name = title['name'],
                                                      name_clean = title['name'],
                                                      lang = title['lang'])
                        firstTitle = False
                    else:
                        fields = splitReview(title['name'])                    
                        saveArticleName = ArticleReview(par_id=saveArticle, 
                                                      full_name=title['name'],
                                                      title=getDef(fields,1, ''),
                                                      author=getDef(fields,0, ''),
                                                      place=getDef(fields,2, ''),
                                                      year=getDef(fields,3, ''),)
                    saveArticleName.save()
                    
                for author in validate['authors']:
                    saveArticleContributor = ArticleContributor(par_id=saveArticle,
                                                                title=author['firstname'] + ' ' + author['surname'],
                                                                firstname=author['firstname'],
                                                                surname=author['surname'],
                                                                role=author['role'])
                    saveArticleContributor.save()
                    if authorStr != '':
                        authorStr += ', '
                    authorStr += author['firstname'] + ' ' + author['surname']
                    
                    
                for page in validate['pages']:
                    saveArticlePage = ArticlePages(par_id=saveArticle,
                                                   page_from=page['page_from'],
                                                   page_to=page['page_to'])
                    saveArticlePage.save()                    
                saveDw = Dw(id = saveArticle.id,
                            title1 = validate['titles'][0]['name'],
                            lang = validate['titles'][0]['lang'],
                            from_field = validate['pages'][0]['page_from'] if len(validate['pages']) > 0 else None,
                            to = validate['pages'][0]['page_to'] if len(validate['pages']) > 0 and validate['pages'][0]['page_to'] != '' else None,
                            idjrl = saveYearName.par_id.journal_id, 
                            journal = (JournalName.objects.filter(par_id=saveYearName.par_id.journal_id))[0].name,
                            idyear = saveYearName.par_id,
                            year = saveYearName.name)
                if saveVolumeName:
                    saveDw.idvol = saveVolumeName.par_id
                    saveDw.volume = saveVolumeName.name
                if saveNumberName:
                    saveDw.idno = saveNumberName.par_id
                    saveDw.number = saveNumberName.name
                if len(validate['titles']) >= 2:
                    saveDw.title2 = validate['titles'][1]['name']    
                publisher = JournalContributor.objects.filter(role='publisher', par_id=saveYearName.par_id.journal_id)
                if publisher:
                    saveDw.publisher = publisher[0].title
                saveDw.authors = authorStr
                saveDw.save()
                
                addPostVar = ''
                if 'add_next' in request.POST:
                    if saveDw.idno:
                        addPostVar = "&number=" + str(saveDw.idno_id)
                    elif saveDw.volume:
                        addPostVar = "&vol=" + str(saveDw.idvol_id)
                    elif saveDw.journal:
                        addPostVar = "&jrl=" + str(saveDw.idjrl_id)                
                    return HttpResponseRedirect(reverse('bib.views.article_mod') + "?mesg=Dodałeś artykuł" + addPostVar)
                
                return HttpResponseRedirect(backToUrl + "?mesg=Dodałeś artykuł" + addPostVar)                 
            else:
                saveArticle = Article.objects.get(pk=id)
                authorStr = ''
                
                if saveNumberName:
                    saveArticle.number_id=saveNumberName.par_id
                else:
                    saveArticle.volume_id=saveVolumeName.par_id
                saveArticle.save()
                
                firstTitle = True
                validIds = []
                for title in validate['titles']:
                    saveArticleName = None
                    if firstTitle:
                        saveArticleName = ArticleName.objects.filter(pk=title['id'])
                        saveArticleName = saveArticleName[0]
                        saveArticleName.name = title['name']
                        saveArticleName.name_clean = title['name']
                        saveArticleName.lang = title['lang'] 
                        firstTitle = False
                    else:
                        fields = splitReview(title['name'])
                                            
                        if title['id']:                        
                            saveArticleName = ArticleReview.objects.filter(pk=title['id'])
                            saveArticleName = saveArticleName[0]
                            saveArticleName.full_name = title['name'] 
                            saveArticleName.author=getDef(fields, 0, '')
                            if '"' in title['name']:
                                saveArticleName.title=u'"' + getDef(fields, 1, '').decode('utf8') + u'"'
                            else:
                                saveArticleName.title=getDef(fields, 1, '')
                            saveArticleName.place=getDef(fields, 2, '')
                            saveArticleName.year=getDef(fields, 3, '')
                        else:
                            saveArticleName = ArticleReview(par_id=saveArticle,
                                                      full_name=title['name'], 
                                                      title=getDef(fields,1, ''),
                                                      author=getDef(fields,0, ''),
                                                      place=getDef(fields,2, ''),
                                                      year=getDef(fields,3, ''),)
                    saveArticleName.save()
                    validIds += [saveArticleName.id]
                for vTitle in ArticleReview.objects.filter(par_id=saveArticle.id):
                    if vTitle.id not in validIds:
                        vTitle.delete() 
                
                validIds = []    
                for author in validate['authors']:                                        
                    if author['id']:
                        saveArticleContributor = ArticleContributor.objects.filter(pk=author['id'])                                        
                        saveArticleContributor = saveArticleContributor[0]
                        saveArticleContributor.title=author['firstname'] + ' ' + author['surname']
                        saveArticleContributor.firstname=author['firstname']
                        saveArticleContributor.surname=author['surname']
                        saveArticleContributor.role=author['role']
                    else:
                        saveArticleContributor = ArticleContributor(par_id=saveArticle,
                                                                title=author['firstname'] + ' ' + author['surname'],
                                                                firstname=author['firstname'],
                                                                surname=author['surname'],
                                                                role=author['role'])
                    if authorStr != '':
                        authorStr += ', '
                    authorStr += author['firstname'] + ' ' + author['surname']
                    saveArticleContributor.save()
                    validIds += [saveArticleContributor.id]
                for vRec in ArticleContributor.objects.filter(par_id=saveArticle.id):
                    if vRec.id not in validIds:
                        vRec.delete()
                
                validIds = []    
                for page in validate['pages']:                    
                    if page['id']:       
                        saveArticlePage = ArticlePages.objects.filter(pk=page['id'])                 
                        saveArticlePage = saveArticlePage[0]
                        saveArticlePage.page_from=page['page_from']
                        saveArticlePage.page_to=page['page_to']
                    else:
                        saveArticlePage = ArticlePages(par_id=saveArticle,
                                                   page_from=page['page_from'],
                                                   page_to=page['page_to'])
                    saveArticlePage.save()
                    validIds += [saveArticlePage.id] 
                for vRec in ArticlePages.objects.filter(par_id=saveArticle.id):
                    if vRec.id not in validIds:
                        vRec.delete()   
                
                saveDw = Dw.objects.get(id=id)
                saveDw.title1 = validate['titles'][0]['name']
                saveDw.lang = validate['titles'][0]['lang']                
                saveDw.from_field = saveArticle.getFirstPageSet().page_from if saveArticle.getFirstPageSet() > 0 else None                
                saveDw.to = saveArticle.getFirstPageSet().page_to if saveArticle.getFirstPageSet() > 0 and saveArticle.getFirstPageSet().page_to != '' else None
                saveDw.idjrl = saveYearName.par_id.journal_id
                saveDw.journal = (JournalName.objects.filter(par_id=saveYearName.par_id.journal_id))[0].name
                saveDw.idyear = saveYearName.par_id
                saveDw.year = saveYearName.name
                if saveVolumeName:
                    saveDw.idvol = saveVolumeName.par_id
                    saveDw.volume = saveVolumeName.name
                else:
                    saveDw.idvol = saveDw.volume = None
                    
                if saveNumberName:
                    saveDw.idno = saveNumberName.par_id
                    saveDw.number = saveNumberName.name
                else:
                    saveDw.idno = saveDw.number = None
                    
                if len(validate['titles']) >= 2:
                    saveDw.title2 = validate['titles'][1]['name']    
                publisher = JournalContributor.objects.filter(role='publisher', par_id=saveYearName.par_id.journal_id)
                if publisher:
                    saveDw.publisher = publisher[0].title
                saveDw.authors = authorStr
                saveDw.save()             
                
                addPostVar = ''
                if 'add_next' in request.POST:
                    if saveDw.idno:
                        addPostVar = "&number=" + str(saveDw.idno_id)
                    elif saveDw.volume:
                        addPostVar = "&vol=" + str(saveDw.idvol_id)
                    elif saveDw.journal:
                        addPostVar = "&jrl=" + str(saveDw.idjrl_id)                   
                    return HttpResponseRedirect(reverse('bib.views.article_mod') + "?mesg=Zmodyfikowałeś artykuł" + addPostVar)
                
                return HttpResponseRedirect(backToUrl + "?mesg=Zmodyfikowałeś artykuł" + addPostVar)    
    else:
        if id != -1:
            article = Article.objects.get(id=id)
            journal = article.sourceWithHier('journal')
            perm = Journalmap.objects.filter(idjrl=journal)
            yearName = ''
            volName = ''
            noName = ''
            if article.sourceWithHier('year'):
                yearName = article.sourceWithHier('year').getName
            if article.sourceWithHier('volume'):
                volName = article.sourceWithHier('volume').getName
            if article.sourceWithHier('number'):
                noName = article.sourceWithHier('number').getName
            if perm:
                formData = {
                            'jrl': journal,
                            'year': yearName,
                            'vol': volName,
                            'no': noName,
                            'titles': ArticleName.objects.filter(par_id=article)[:1],
                            'reviews': ArticleReview.objects.filter(par_id=article),
                            'authors': ArticleContributor.objects.filter(Q(role='author')|Q(role='translator')|Q(role='reviewed_work_author'), par_id=article),
                            'pages': article.getPages,
                            }
                context['formData'] = formData
            else:
                return HttpResponseRedirect(reverse('bib.views.article_mod'))
    #         form = DwForm(instance=dwObj)      
        else:
            formData = {}
            if 'jrl' in request.GET:
                formData = {'jrl': Journal.objects.get(id=request.GET['jrl'])}                   
            elif 'vol' in request.GET:
                getVol = Volume.objects.get(id=request.GET['vol'])
                formData = {
                            'jrl': getVol.sourceWithHier('journal'),
                            'year': getVol.sourceWithHier('year').getName,
                            'vol': getVol.sourceWithHier('volume').getName if getVol.sourceWithHier('volume') else ''
                            }
            elif 'number' in request.GET:
                getNo = Number.objects.get(id=request.GET['number'])
                formData = {
                            'jrl': getNo.sourceWithHier('journal'),
                            'year': getNo.sourceWithHier('year').getName,
                            'vol': getNo.sourceWithHier('volume').getName if getNo.sourceWithHier('volume') else '',
                            'no': getNo.sourceWithHier('number').getName if getNo.sourceWithHier('number') else '',
                            }
            context['formData'] = formData
    return render_to_response(templates['article_mod'], context)

def passwordReset(request):
    context = RequestContext(request, {    
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'],
            'request': request,
            # 'extraJs': [meta['scripts']['select']],
        })
    form = passwordResetForm()
    if request.POST:
        form = passwordResetForm(request.POST)
        if form.is_valid():
            if not User.objects.filter(email=form['username'].value()).exists():
                context['mesg'] = u'Podano nieprawidłowy adres email.'
                return render_to_response(templates['mesg'], context)
            userObj = User.objects.get(email=form['username'].value())
            PasswordReset.objects.filter(user=userObj).delete()
            passwordReset = PasswordReset(user=userObj,
                                          password=form['password'].value())
            passwordReset.save()
            context['mesg'] = u'Wysłano monit o zresetowanie hasła na twoją skrzynkę pocztową.'
            t = loader.get_template(templates['passReset_email'])
            md5_hash = md5.new(form['password'].value())
            c = Context ({'key': md5_hash.hexdigest(),
                          'userid': userObj.pk })
            subject = u'Resetowanie hasła w serwisie www.bazhum.pl'
            send_mail(subject, 
                       t.render(c),
                       'webmaster@bazhum.pl',
                       [form['username'].value()],
                       fail_silently=False )
            return render_to_response(templates['mesg'], context)
        else:
            context['mesg'] = u'Błędnie wypełniony formularz.'
            return render_to_response(templates['mesg'], context)          
    else:
        context['form'] = form
    return render_to_response(templates['passwordReset'], context)

def passwordResetConfirm(request, userid, key):
    userObj = User.objects.get(id=userid)
    prObj = PasswordReset.objects.get(user=userObj)
    md5Obj = md5.new(prObj.password)
    if key == md5Obj.hexdigest():
        userObj.set_password(prObj.password)
        userObj.save()
        mesg = u'Pomyślnie zmieniono hasło.'
    else:
        mesg = u'Nie udało się zmienić hasła.'
    context = RequestContext(request, {    
            'templ': templates, 
            'mesg': mesg,
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'],
            'request': request,
            # 'extraJs': [meta['scripts']['select']],
        })
    return render_to_response(templates['mesg'], context)

def listPub(request, id):
    publisher = JournalContributor.objects.get(id=id)    
    if not publisher:
        publisher = JournalContributor.objects.get(id=1)
    selIds = JournalContributor.objects.filter(title=publisher.title, role='publisher')
    journals = Journal.objects.filter(id__in=selIds.values_list('par_id', flat=True))
    context = RequestContext(request, {
            'publisher': publisher,
            'jrls': journals,    
            'templ': templates, 
            'ehself_count': eshelfCount(request),
            'meta': meta,
            'title': meta['title'],
            'request': request,
            # 'extraJs': [meta['scripts']['select']],
        })
    return render_to_response(templates['list_pub'], context)
    
def searchAuthors(request):
#     return HttpResponse(str([1,2,3]))    
    arr = '['
    for rec in ArticleContributor.objects.filter(title__icontains=request.GET.get('term', '')).distinct().values_list('title', flat=True):
        arr += '"' + rec + '",'
    arr += ']'
    return HttpResponse(arr)
                                             