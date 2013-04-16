# -*- coding: utf-8 -*-

from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from bib.models import *

class JournalListFilter(SimpleListFilter):
    title = _('journal')

    parameter_name = 'journal'

    def lookups(self, request, model_admin):
        self.query_string = {}
        self.request = {}
        lc_list = {}
        for rec in JournalName.objects.all().order_by('par_id'):
			if hasattr(rec, 'par_id') and hasattr(rec.par_id, 'id'):
				if rec.par_id.id not in lc_list:
					lc_list[rec.par_id.id] = rec.name

        ll = lc_list.items()
        ll = sorted_by_second = sorted(ll, key=lambda tup: tup[1])
        return ll

    def queryset(self, request, queryset):
        if 'journal' not in request.GET:
            return queryset
        var1 = Article.objects.filter(number_id__volume_id__year_id__journal_id__id=self.value)        
        var2 = Article.objects.filter(volume_id__year_id__journal_id__id=self.value)
        var3 = Article.objects.filter(number_id__year_id__journal_id__id=self.value)        
        return var1 | var2 | var3
        
class YearListFilter(SimpleListFilter):
    title = _('year')

    parameter_name = 'year'

    def lookups(self, request, model_admin):
        if 'journal' not in request.GET:
            return None
        lc_list = {}
        for rec in Year.objects.filter(journal_id=request.GET['journal']).order_by('id'):
            if rec.id not in lc_list:
                lc_list[rec.id] = rec.__unicode__()

        ll = lc_list.items()
        ll = sorted_by_second = sorted(ll, key=lambda tup: tup[1])
        return ll

    def queryset(self, request, queryset):
        if 'year' not in request.GET:
            return queryset.all()
        var1 = Article.objects.filter(number_id__volume_id__year_id__id=self.value)        
        var2 = Article.objects.filter(volume_id__year_id__id=self.value)
        var3 = Article.objects.filter(number_id__year_id__id=self.value)        
        return var1 | var2 | var3
        
class VolumeListFilter(SimpleListFilter):
    title = _('volume')

    parameter_name = 'volume'

    def lookups(self, request, model_admin):
        if 'year' not in request.GET:
            return None
        lc_list = {}
        for rec in Volume.objects.filter(year_id=request.GET['year']).order_by('id'):
            if rec.id not in lc_list:
                lc_list[rec.id] = rec.__unicode__()

        ll = lc_list.items()
        ll = sorted_by_second = sorted(ll, key=lambda tup: tup[1])
        return ll

    def queryset(self, request, queryset):
        if 'volume' not in request.GET:
            return queryset.all()
        var1 = Article.objects.filter(number_id__volume_id__id=self.value)        
        var2 = Article.objects.filter(volume_id__id=self.value)
        return var1 | var2
        
class NumberListFilter(SimpleListFilter):
    title = _('number')

    parameter_name = 'number'

    def lookups(self, request, model_admin):
        if 'volume' not in request.GET:
            if 'year' not in request.GET:
                return None
            else:
                # search by year
                lc_list = {}
                for rec in Number.objects.filter(year_id=request.GET['year']).order_by('id'):
                    if rec.id not in lc_list:
                        lc_list[rec.id] = rec.__unicode__()

                ll = lc_list.items()
                ll = sorted_by_second = sorted(ll, key=lambda tup: tup[1])
                return ll
        else:
            # search by volume
            lc_list = {}
            for rec in Number.objects.filter(volume_id=request.GET['volume']).order_by('id'):
                if rec.id not in lc_list:
                    lc_list[rec.id] = rec.__unicode__()

            ll = lc_list.items()
            ll = sorted_by_second = sorted(ll, key=lambda tup: tup[1])
            return ll

    def queryset(self, request, queryset):
        if 'volume' not in request.GET:
            if 'year' not in request.GET:
                return queryset.all() 
        return Article.objects.filter(number_id__id=self.value)         