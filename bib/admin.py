# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models.loading import get_model
from django.http import HttpResponseRedirect

from bib.models import *
from bib.filters import *
from bib.forms import *
from bib.fieldTypes import aff_mod

from django.core import urlresolvers
import reversion

class baseBibAdmin(reversion.VersionAdmin):
    # fieldName, model, nameObject, parents
    allowedKeys = (
            (u'journal_id', Journal, u'journalname__name', () ),
            (u'year_id', Year, u'yearname__name', (u'journal_id',) ),
            (u'volume_id', Volume, u'volumename__name', (u'year_id',) ),
            (u'number_id', Number, u'numbername__name', (u'volume_id', u'year_id') ),
            (u'article_id', Article, u'articlename__name', (u'number_id', u'volume_id') ),
        )

    def changelist_view(self, request, extra_context={}):
        for k,v in request.GET.iteritems():
            if k in [x[0] for x in self.allowedKeys]:                
                extra_context['addVars'] = k + '=' + v + '&'
        return super(baseBibAdmin, self).changelist_view(request, extra_context)
    
    def get_object_from_url(self, request):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        model_name = request.META['PATH_INFO'].strip('/').split('/')[-2]
        app_name = request.META['PATH_INFO'].strip('/').split('/')[-3]
        try:
            object_id = int(object_id)
            model = get_model(app_name, model_name)
        except ValueError:
            return None
        return model.objects.get(pk=object_id)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        for fn, mod, nameObj, parents in self.allowedKeys:            
            if db_field.name == fn:
                obj = self.get_object_from_url(request)
                if obj:
                    parObj = None
                    if hasattr(obj, fn):
                        parObj = getattr(obj, fn)
                    if parObj is not None:
                        for parentField in parents:
                            criteria = {parentField: getattr(parObj, parentField)}
                            queryset = mod.objects.filter(**criteria).order_by(nameObj)
                            return aff_mod(mod, (('All',{}),), queryset, required=False )
                if fn == u'journal_id':
                    queryset = mod.objects.all().order_by(nameObj)
                    return aff_mod(mod, (('All',{}),), queryset, required=False )
                else:
                    for parent in parents:
                        if fn in request.GET:
                            parObj = mod.objects.get(id=request.GET[fn])
                            criteria = {parent: getattr(parObj, parent)}
                            queryset = mod.objects.filter(**criteria).order_by(nameObj)
                            return aff_mod(mod, (('All',{}),), queryset, required=False )
                            
                queryset = mod.objects.none()
                
                return aff_mod(mod, (('All',{}),), queryset, required=False)
        return super(baseBibAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    def response_add(self, request, obj, post_url_continue=None):
        if not '_continue' in request.POST:
            getvar = u'?'
            for k,v in request.GET.iteritems():
                getvar += k + '=' + v + '&'
            url = urlresolvers.reverse('admin:{0}_{1}_changelist'.format(obj._meta.app_label, obj._meta.module_name), args=()) + getvar
            return HttpResponseRedirect(url)
        else:
            return super(baseBibAdmin, self).response_add(request, obj, url)

    def response_change(self, request, obj):
        if not '_continue' in request.POST:
            getvar = '?'
            for fn, mod, nameObj, parents in self.allowedKeys:
                if mod._meta.module_name == obj._meta.module_name:
                    for parent in parents:
                        if hasattr(obj, parent):
                            getValue = getattr(obj, parent)
                            if getValue:
                                getvar += parent + "=" + unicode(getValue.id) +"&"
            url = urlresolvers.reverse('admin:{0}_{1}_changelist'.format(obj._meta.app_label, obj._meta.module_name), args=()) + getvar
            return HttpResponseRedirect(url)
        else:
            return super(baseBibAdmin, self).response_change(request, obj)

class ArticleNameInline(admin.TabularInline):
    fields = ['name', 'lang']
    extra = 0
    model = ArticleName
    
class ArticleContributorInline(admin.StackedInline):
    fields = ['title', 'firstname', 'surname', 'role']
    extra = 0
    model = ArticleContributor
    
class ArticleDateInline(admin.TabularInline):
    fields = ['type', 'text']
    extra = 0
    model = ArticleDate
    
class ArticleDescriptionInline(admin.TabularInline):
    fields = ['text', 'lang']
    extra = 0
    model = ArticleDescription
    
class ArticleKeywordsInline(admin.TabularInline):
    fields = ['kw', 'lang']
    extra = 0
    model = ArticleKeywords
    
class ArticleReferencesInline(admin.TabularInline):
    fields = ['text']
    extra = 0
    model = ArticleReferences
    
class ArticlePagesInline(admin.TabularInline):
    fields = ['page_from', 'page_to']
    extra = 0
    model = ArticlePages

class ArticleAdmin(baseBibAdmin):
    list_display = ['nazwa', 'bibliographical_description', 'source']
    search_fields = ['articlename__name', ]
        # 'number_id__numbername__name', 
        # 'volume_id__volumename__name', 'number_id__volume_id__volumename__name',
        # 'number_id__volume_id__year_id__yearname__name', 'volume_id__year_id__yearname__name', 
        # 'volume_id__year_id__journal_id__journalname__name', 'number_id__volume_id__year_id__journal_id__journalname__name',]
    list_filter = [JournalListFilter, YearListFilter, VolumeListFilter]
    inlines = [ArticleNameInline, ArticlePagesInline, ArticleDescriptionInline, ArticleDateInline, ArticleContributorInline, ArticleKeywordsInline, ArticleReferencesInline]
    readonly_fields = ['id', 'legacy_id', 'parent']

    def nazwa (self, obj):
        names = ArticleName.objects.filter(par_id=obj.id)
        return names[0].name if names else obj.id
    nazwa.allow_tags = True
    nazwa.short_description = 'Nazwa'

class NumberNameInline(admin.TabularInline):
    fields = ['name', 'lang']
    extra = 0
    model = NumberName
    
class NumberContributorInline(admin.StackedInline):
    fields = ['title', 'firstname', 'surname', 'role']
    extra = 0
    model = NumberContributor
        
class NumberAdmin(baseBibAdmin):
    #form = NumberForm
    inlines = [NumberNameInline, NumberContributorInline]
    list_display = ['source', 'showArticle']
    readonly_fields = ['id', 'legacy_id', 'parent']
    
    def showArticle(self, obj):
        cnt = Article.objects.filter(number_id=obj.id).count()
        return u'<a href="{0}?number_id={1}">Artykuły ({2})</a>'.format(urlresolvers.reverse('admin:bib_article_changelist', args=()), obj.id, cnt)
    showArticle.allow_tags = True
    showArticle.short_description = 'Artykuły'

class VolumeNameInline(admin.TabularInline):
    fields = ['name', 'lang']
    extra = 0
    model = VolumeName
    
class VolumeContributorInline(admin.StackedInline):
    fields = ['title', 'firstname', 'surname', 'role']
    extra = 0
    model = VolumeContributor

class VolumeAdmin(baseBibAdmin):
    #form = VolumeForm
    inlines = [VolumeNameInline, VolumeContributorInline]
    list_display = ['source', 'showNumber', 'showArticle']
    readonly_fields = ['id', 'legacy_id', 'parent']    
    
    def showNumber(self, obj):
        cnt = Number.objects.filter(volume_id=obj.id).count()
        return u'<a href="{0}?volume_id={1}">Numery ({2})</a>'.format(urlresolvers.reverse('admin:bib_number_changelist', args=()), obj.id, cnt)
    showNumber.allow_tags = True
    showNumber.short_description = 'Numery'
    
    def showArticle(self, obj):
        cnt = Article.objects.filter(volume_id=obj.id).count()
        return u'<a href="{0}?volume_id={1}">Artykuły ({2})</a>'.format(urlresolvers.reverse('admin:bib_article_changelist', args=()), obj.id, cnt)
    showArticle.allow_tags = True
    showArticle.short_description = 'Artykuły'

class YearNameInline(admin.TabularInline):
    fields = ['name', 'lang']
    extra = 0
    model = YearName
    
class YearContributorInline(admin.StackedInline):
    fields = ['title', 'firstname', 'surname', 'role']
    extra = 0
    model = YearContributor

class YearDateInline(admin.StackedInline):
    fields = ['type', 'text']
    extra = 0
    model = YearDate   
    
# class YearAdmin(reversion.VersionAdmin):
class YearAdmin(baseBibAdmin):
    #form = YearForm
    inlines = [YearNameInline, YearContributorInline, YearDateInline]
    list_display = ['source', 'showVolume', 'showNumber']
    readonly_fields = ['id', 'legacy_id', 'parent']
    list_filter = ['journal_id']
    search_fields = ['journal_id__journalname__name']
    
    def showVolume(self, obj):
        cnt = Volume.objects.filter(year_id=obj.id).count()
        return '<a href="{0}?year_id={1}">Tomy ({2})</a>'.format(urlresolvers.reverse('admin:bib_volume_changelist', args=()), obj.id, cnt)
    showVolume.allow_tags = True
    showVolume.short_description = 'Tomy'
    
    def showNumber(self, obj):
        cnt = Number.objects.filter(year_id=obj.id).count()
        return '<a href="{0}?year_id={1}">Numery ({2})</a>'.format(urlresolvers.reverse('admin:bib_number_changelist', args=()), obj.id, cnt)
    showNumber.allow_tags = True
    showNumber.short_description = 'Numery'

class JournalNameInline(admin.TabularInline):
    fields = ['name', 'lang']
    extra = 0
    model = JournalName
    
class JournalContributorInline(admin.StackedInline):
    fields = ['title', 'firstname', 'surname', 'role']
    extra = 0
    model = JournalContributor

class JournalDateInline(admin.StackedInline):
    fields = ['type', 'text']
    extra = 0
    model = JournalDate   
    
class JournalAdmin(reversion.VersionAdmin):
    #form = JournalForm
    inlines = [JournalNameInline, JournalContributorInline, JournalDateInline]
    list_display = ['source', 'showYear']
    list_filter = ['journalname', 'journaldate', 'journalcontributor']
    search_fields = ['journalname__name', 'journaldate__text', 'journalcontributor__title']
    readonly_fields = ['id', 'legacy_id', 'parent']
    
    def showYear(self, obj):
        yearCnt = Year.objects.filter(journal_id=obj.id).count()
        return '<a href="{0}?journal_id={1}">Roczniki ({2})</a>'.format(urlresolvers.reverse('admin:bib_year_changelist', args=()), obj.id, yearCnt)
    showYear.allow_tags = True
    showYear.short_description = 'Roczniki'
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Number, NumberAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Journal, JournalAdmin)
