# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from bib.models import *
from bib.util import *

class searchFeed(Feed):
    title = "BazHum"
    link = "http://www.bazhum.pl/bib/rss/"
    description = "Kwerenda na www.bazhum.pl"

    def get_object(self, request):
        qs = Dw.objects.all()
        qs = processQuery(qs, request)
        return qs
    
    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.title1

    def item_description(self, item):
        return item.getSourceName()

    def item_link(self, item):
        return 'http://www.bazhum.pl' + reverse('bib.views.showArticle', args=[item.id])