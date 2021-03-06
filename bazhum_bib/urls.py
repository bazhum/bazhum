# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

js_info_dict = {
    'packages': ('bazhum_bib.bib',),
}

urlpatterns = patterns('',    
    (r'^ajax_filtered_fields/', include('ajax_filtered_fields.urls')),
    # Examples:
    # url(r'^$', 'bazhum_bib.views.home', name='home'),
    # url(r'^bazhum_bib/', include('bazhum_bib.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    # (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        # {'document_root': '/srv/www/python/django-1.5-env/www/bazhum_bib_dev/media/'}),   
	# (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        # {'document_root': '/srv/www/python/django-1.5-env/www/bazhum_bib_dev/bib/static/'}),   
	(r'^bib/', include('bib.urls')),
    (r'^$', 'bib.views.main'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),    
#     (r'^accounts/', include('registration.backends.default.urls')),
)
