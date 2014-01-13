# -*- coding: utf-8 -*-

from bib.models import *
from django.db.models import Q
import _mysql
import re
from StringIO import StringIO
from csv import reader
import codecs



def prepNameForPath(str):
    result = str    
    ins = [u'ę', u'ó', u'ą', u'ś', u'ł', u'ż', u'ź', u'ć', u'ń']
    outs = [u'e', u'o', u'a', u's', u'l', u'z', u'z', u'c', u'n']
    for x in range(len(ins)):
        result = result.replace(ins[x], outs[x])
             
    result = re.sub('[^a-zA-Z0-9()]+', '_', result)
    return result

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
    
def exportTxt (qs, format):
    result = ''
    sortQuery = []
    for obj in qs:
        if isinstance(obj, basestring):
            continue
#             if ArticleReview.objects.filter(par_id=obj.id).count() > 0:
#                 continue
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
        sortQuery += [{
            'id': obj.id, 
            'authors': authors, 
            'title': title.name_clean, 
            'year': yearName, 
            'volume': volumeName, 
            'number': numberName, 
            'journal': journal.__unicode__(), 
            'pages': pages,
            }]

    sortQuery = sorted(sortQuery, key=lambda k: yearNameConv(k['year']))
    sortQuery = sorted(sortQuery, key=lambda k: yearNameConv(k['volume']))
    sortQuery = sorted(sortQuery, key=lambda k: numberNameConv(k['number']))
        
    for obj in sortQuery:
        if format == 'bibtex':
            result += ''' @Article{%s, 
                     author = "%s",
                     title = "%s",
                     year =  %s,
                     volume =  %s,
                     number =  %s,
                     journal =  %s,
                     pages =  %s,
                    }\n '''  % (obj['id'], obj['authors'], obj['title'], obj['year'], obj['volume'], obj['number'], obj['journal'], obj['pages'])
                    
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
%s ''' % (obj['authors'], obj['title'], obj['year'], obj['volume'], obj['number'], obj['journal'], pages)
    return result
    
def numberNameConv(str):
    if str:
        if not isinstance(str, basestring):
            str = str.__unicode__()
    else:
        if not str:
            return ''
        return str
    
    res = str
    if '-' in str:
        str = str.split('-')[0]
        str = str.split('/')[0]
    elif ' ' in str:
        str = str.split(' ')[0]
    try:
        res = int(re.sub('[^0-9]+', '', str))
    except ValueError:
        res = str
    return res
    
def yearNameConv(str):
    if not isinstance(str, basestring):
        res = str.name
        str = str.name
    else:
        res = str
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
    
def processQuery (qs, request, pagination={'from': None, 'to': None}):
    # main query
    
    # publisher query
    if 'pub' in request.GET:
        qs = Dw.objects.filter(publisher=request.GET['pub'])
        
    elif 'generalQuery' in request.GET:
        queryStr = addObligMysql(request.GET['generalQuery'])
        titleSearch = Q(title1__search=queryStr)
        journalSearch = Q(journal__search=queryStr)
        qs = Dw.objects.filter(titleSearch | journalSearch)
        
    # advanced query    
    elif 'typeField' in request.GET:
        if 'mode' in request.GET:
            mode = request.GET['mode']
        else:
            mode = 'all'

        addqs = Dw.objects.none()
        tmpqs = Dw.objects.none()
        
        valList = request.GET.getlist('valueField')
        if len(valList) == 0:
            return Dw.objects.none()
        
        for type in request.GET.getlist('typeField'):
            if valList:            
                if type <> 'date':
                    if valList[0] == '':
                        valList.pop(0)
                        continue
                else:            
                    if valList[0] == '' and valList[1] == '':
                        valList.pop(0)
                        valList.pop(0)
                        continue
                        
            if type == 'any':
                queryStr = addObligMysql(valList.pop(0))
                titleSearch = Q(title1__search=queryStr)
                journalSearch = Q(journal__search=queryStr)
                tmpqs = Dw.objects.filter(titleSearch | journalSearch)
                if mode == 'any':
                    addqs = addqs | tmpqs
                else:
                    qs = tmpqs
            elif type == 'title':
                if mode == 'any':
                    addqs = addqs | qs.filter(title1__search=addObligMysql(valList.pop(0)))
                else:
                    qs = qs.filter(title1__search=addObligMysql(valList.pop(0)))                
            elif type == 'author':
                if mode == 'any':
                    addqs = addqs | qs.filter(authors__search=addObligMysql(valList.pop(0)))
                else:
                    qs = qs.filter(authors__search=addObligMysql(valList.pop(0)))
            elif type == 'jrl':
                if mode == 'any':
                    addqs = addqs | qs.filter(journal__search=addObligMysql(valList.pop(0))) 
                else:
                    qs = qs.filter(journal__search=addObligMysql(valList.pop(0))) 
            elif type == 'date':
                yFrom = _mysql.escape_string(valList.pop(0))
                yTo = _mysql.escape_string(valList.pop(0))
                years = Dw.objects.none()
                from warnings import filterwarnings
                import MySQLdb as Database
                filterwarnings('ignore', category = Database.Warning)
                
                if yFrom <> '' and yTo <> '':                    
                    years = Dw.objects.extra(where=["cast(year as signed) >= " + yFrom + " and cast(year as signed) <= " + yTo])
                elif yFrom <> '' and yTo == '':
                    years = Dw.objects.extra(where=["cast(year as signed) >= " + yFrom])
                elif yFrom == '' and yTo <> '':
                    years = Dw.objects.extra(where=["cast(year as signed) <= " + yTo])
                    
                if mode == 'any':
                    addqs = addqs | years
                else:
                    qs = qs.filter(id__in=years)

            elif type == 'lang':
                if valList[0] != 'XX':
                    if mode == 'any':
                        addqs = addqs.distinct() | qs.filter(lang=valList.pop(0)).distinct()
                    else:
                        qs = qs.filter(lang=valList.pop(0)).distinct()
    
        if mode == 'any':
            qs = addqs
            
    return qs

def processQueryFilters(qs, request, pagination={'from': None, 'to': None}):
    sqs = Dw.objects.none()
    if 'fa' in request.GET:
        for faInst in request.GET.getlist('fa'):
            if ArticleContributor.objects.filter(title=faInst):
                tmpAuthor = ArticleContributor.objects.filter(title=faInst)[0]
                sqs = sqs | qs.filter(authors__icontains=tmpAuthor.getCustomTitle)
#                 sqs = sqs | qs.filter(authors__icontains=faInst)
        qs = sqs
    sqs = Dw.objects.none()
    if 'fj' in request.GET:
        for fjInst in request.GET.getlist('fj'):
            sqs = sqs | qs.filter(idjrl=fjInst)
        qs = sqs
    sqs = Dw.objects.none()
    if 'fl' in request.GET:
        for flInst in request.GET.getlist('fl'):
            sqs = sqs | qs.filter(lang=flInst)
        qs = sqs
    sqs = Dw.objects.none()
    if 'fFrom' in request.GET:
        fromInst = request.GET.getlist('fFrom')
        toInst = request.GET.getlist('fTo')
        for x in range(0, len(fromInst)):
            yFrom = fromInst[x]
            yTo = toInst[x]                     
            sqs = sqs | qs.filter(Q(year__lte=yTo) & Q(year__gte=yFrom))
        qs = sqs
    return qs

def processQueryPagination(qs, pagination={'from': None, 'to': 20}):
    return qs[pagination['from']:pagination['to']]
    
def prepareResultRecord(qs):
    results = []
    for article in qs[:20]:        
        fullArticle = {
                'article': article,
                'pages': ArticlePages.objects.filter(par_id=article.id),
                'journal': article.sourceWithHier('journal'),
                'year': article.sourceWithHier('year'),
                'volume': article.sourceWithHier('volume'),
                'number': article.sourceWithHier('number'),                                
            }
        results += [fullArticle]
    return results

def parsSelUrl(request):
    if request.GET.get('ids', '') == "" and request.GET.get('idsSec', '') == "":
        result = 'Musisz zaznaczyć obiekty do eksportu !'
        title = 'brak_zaznaczenia'
    # export from publisher menu
    elif request.GET['idsType'] == 'journal':
        idsArray = request.GET['ids'].split(',')
        idsArticles = Dw.objects.filter(idjrl__in=idsArray).values_list('id', flat=True).distinct()
        articles = Article.objects.filter(id__in=idsArticles)
        result = articles
        if len(idsArray) > 1:
            title = 'wiele_czasopism'
        else:
            title = (JournalName.objects.filter(par_id=idsArray[0]))[0].name
    # journal level export
    elif request.GET['idsType'] == 'vol':
        title = 'Rocznik'
        volumes = []
        numbers = []
        if not 'y' in request.GET['ids']:
            volumes = Volume.objects.filter(id__in=request.GET['ids'].split(','))        
            numbers = Number.objects.filter(volume_id__in=volumes)
            title = volumes[0].year_id.journal_id.__unicode__()
        else:
            numbers = Number.objects.filter(year_id__in=re.sub('y','',request.GET['ids']).split(','))
            title = numbers[0].year_id.journal_id.__unicode__()
        articles = Article.objects.filter(Q(volume_id__in=volumes) | Q(number_id__in=numbers))
        
        # years = sorted(Year.objects.filter(journal_id=jrl), key=lambda a: yearNameConv(a.getName), reverse=True)
        # articles = sorted(Year.objects.filter(journal_id=jrl), key=lambda a: yearNameConv(a.getName), reverse=True)
        # numberNames = sorted(NumberName.objects.filter(par_id__in=numbers), key=lambda a: numberNameConv(a.name))
        # numberNames = sorted(NumberName.objects.filter(par_id__in=numbers), key=lambda a: numberNameConv(a.name))
        
        result = articles        
        # title = volumes[0].year_id.__unicode__()
    # volume level export
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
        articles = Article.objects.filter(Q(number_id__in=numbers) | Q(id__in=artIds)).order_by('number_id', 'id')
        result = articles
        if title == 'tom':
            if articles[0].volume_id:
                title = articles[0].volume_id.__unicode__()
            elif articles[0].number_id:
                title = articles[0].number_id.__unicode__()            
    # article level export
    else:
        artQs = Article.objects.filter(id__in=request.GET['ids'].split(','))
        result = artQs
        title = artQs[0].__unicode__()
        
    #result = result.filter(id__in=Dw.objects.filter(accepted=True).values_list(id, flat=True))
#     result = result.filter(id__in=Dw.objects.values_list(id, flat=True))
    return {'articles': result, 'title': title}

def eshelfCount(request):
    rUser = request.user
    if rUser.is_authenticated():
        return Eshelf.objects.filter(user=rUser).count()
    else:
        return 0
    
def in_lib_group(user):
    if user:
        return user.groups.filter(name='lib').count() > 0
    return False

def in_pub_group(user):
    if user:
        return user.groups.filter(name='pub').count() > 0
    return False

def in_admin_group(user):
    if user:
        if in_lib_group(user) or in_pub_group(user):
            return True
    else:
        False

def getJrlPerms(request):
    jrlPerms = None
    if request.user.is_authenticated():
        jrlPerms = Journalmap.objects.filter(iduser=request.user).values_list('idjrl', flat=True)
    return jrlPerms

def splitReview(str):
    result = []
    file_like_object = StringIO(str.encode('utf8'))
#     codecinfo = codecs.lookup("utf8")
#     file_like_object = codecs.StreamReaderWriter(file_like_object, 
#         codecinfo.streamreader, codecinfo.streamwriter)
    csv_reader = reader(file_like_object, quotechar='"', skipinitialspace=True)
    for row in csv_reader:
        return row
    return result

def getDef(arr, index, defVal):
    if index < len(arr):
        return arr[index].strip()
    else:
        return defVal