# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from bib.feed import *

urlpatterns = patterns(
    '',
    # (r'^pageChg/$', 'bib.views.pageChg'),
    (r'^$', 'bib.views.main'),
    (r'^search/advanced/$', 'bib.views.searchAdvanced'),
    (r'^search/results/$', 'bib.views.searchResults'),
    (r'^about/$', 'bib.views.about'),
    (r'^list/$', 'bib.views.journalList'),
    (r'^journal/(\d+)/$', 'bib.views.showJournal'),
    (r'^volume/(\d+)/$', 'bib.views.showVolume'),
    (r'^number/(\d+)/$', 'bib.views.showNumber'),
    (r'^article/(\d+)/$', 'bib.views.showArticle'),
	(r'^ajax/$', 'bib.views.servAjax'),
    (r'^export/$', 'bib.views.export'),
    (r'^rss/$', searchFeed()),
)