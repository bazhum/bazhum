# -*- coding: utf-8 -*-

from django.conf.urls import *
from bib.feed import *

js_info_dict = {
    'packages': ('bazhum_bib.bib',),
}

urlpatterns = patterns(
    '',
    # (r'^pageChg/$', 'bib.views.pageChg'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    (r'^search/advanced/$', 'bib.views.searchAdvanced'),
    (r'^search/results/mobile/$', 'bib.views.searchResultsMobile'),
    (r'^search/results/$', 'bib.views.searchResults'),
    (r'^about/$', 'bib.views.about'),
    (r'^list/$', 'bib.views.journalList'),
    (r'^publisher/list/(\d+)/$', 'bib.views.listPub'),
    (r'^journal/(\d+)/$', 'bib.views.showJournal'),
    (r'^volume/(\d+)/$', 'bib.views.showVolume'),
    (r'^number/(\d+)/$', 'bib.views.showNumber'),
    (r'^article/(\d+)/$', 'bib.views.showArticle'),
    (r'^article/mod/(\d+)/$', 'bib.views.article_mod'),
    (r'^article/mod/$', 'bib.views.article_mod'),
	(r'^ajax/$', 'bib.views.servAjax'),
    (r'^export/$', 'bib.views.export'),
    (r'^register/$', 'bib.views.registerView'),
    (r'^logout/$', 'bib.views.logoutView'),
    (r'^login/$', 'bib.views.loginView'),
    (r'^passwordReset/$', 'bib.views.passwordReset'),
    (r'^passwordReset/(\d+)/(\w+)/$', 'bib.views.passwordResetConfirm'),
    (r'^activate/(\w+)/$', 'bib.views.activate'),
    (r'^e_shelf/$', 'bib.views.e_shelf'),    
    (r'^e_shelf/(\d+)/$', 'bib.views.e_shelf'),
    (r'^e_shelf/(\d+)/(\d+)/$', 'bib.views.e_shelf'),
    (r'^list/librarian/$', 'bib.views.list_librarian'),
    (r'^list/publisher/$', 'bib.views.list_publisher'),
    (r'^rss/$', searchFeed()),
    (r'authorsSearch/$', 'bib.views.searchAuthors')    
)