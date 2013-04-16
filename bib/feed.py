# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from bib.models import *
from bib.views import addObligMysql

class searchFeed(Feed):
    title = "BazHum"
    link = "http://www.bazhum.pl/bib/rss/"
    description = "Kwerenda na www.bazhum.pl"

    def get_object(self, request):
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
                        addqs = addqs | qs.filter(articlename__lang=valList.pop(0)).distinct()
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
        return qs
    
    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.getName

    def item_description(self, item):
        return item.source

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return 'http://www.bazhum.pl' + reverse('bib.views.showArticle', args=[item.id])