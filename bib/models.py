# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# base clases & func

# def exportTxt (qs, format):
#     from bib.util import yearNameConv, numberNameConv, prepNameForPath
#     result = ''
#     sortQuery = []
#     for obj in qs:
# #         if not isinstance(obj, basestring):
# #             if ArticleReview.objects.filter(par_id=obj.id).count() > 0:
# #                 continue
#         authors = []
#         for auth in ArticleContributor.objects.filter(par_id=obj.id, role='author'):
#             authors += [auth.title]
#         authors = ', '.join([x for x in authors])
#         if ArticleName.objects.filter(par_id=obj.id).count() > 0:
#             title = (ArticleName.objects.filter(par_id=obj.id))[0]
#         number = obj.sourceWithHier('number')
#         yearName = ''
#         volumeName = ''
#         numberName = ''
#         if number:
#             numberName = number.getName
#         volume = obj.sourceWithHier('volume')
#         if volume:
#             volumeName = volume.getName
#         year = obj.sourceWithHier('year')
#         if year:
#             yearName = year.getName
#         journal = obj.sourceWithHier('journal')
#         pagesA = []
#         for page in ArticlePages.objects.filter(par_id=obj.id):
#             pagesA += [page]
#         pages = 's.' + ','.join(map(unicode,pagesA))
#         sortQuery += [{
#             'id': obj.id, 
#             'authors': authors, 
#             'title': title.name_clean, 
#             'year': yearName, 
#             'volume': volumeName, 
#             'number': numberName, 
#             'journal': journal.__unicode__(), 
#             'pages': pages,
#             }]
#  
#     sortQuery = sorted(sortQuery, key=lambda k: yearNameConv(k['year']))
#     sortQuery = sorted(sortQuery, key=lambda k: yearNameConv(k['volume']))
#     sortQuery = sorted(sortQuery, key=lambda k: numberNameConv(k['number']))
#          
#     for obj in sortQuery:
#         if format == 'bibtex':
#             result += '''@Article{%s, 
#  author = "%s",
#  title = "%s",
#  year =  %s,
#  volume =  %s,
#  number =  %s,
#  journal =  %s,
#  pages =  %s,
# }\n '''  % (obj['id'], obj['authors'], obj['title'], obj['year'], obj['volume'], obj['number'], obj['journal'], obj['pages'])
#         elif format == 'txt':
#             result += '''%s, %s, %s, %s, %s, %s ''' % (obj['title'], obj['journal'], obj['year'], obj['volume'], obj['number'], obj['pages'])
#         elif format == 'ris':
#             pages = ''
#             for p in pagesA:
#                 pages += 'SP - ' + p.page_from + '\n'
#                 pages += 'EP - ' + p.page_to + '\n'
#             result += ''' 
# TY  - JOUR 
# AU - %s
# TI - %s
# PY - %s
# VL - %s
# NV - %s
# JO - %s 
# %s ''' % (obj['authors'], obj['title'], obj['year'], obj['volume'], obj['number'], obj['journal'], pages)
     
#     return result

def getName(self, nameObj):
    names = nameObj.objects.filter(par_id=self)
    if not names:
        return ''
    if isinstance(nameObj, ArticleName):
        return names[0].clean_name if names else self.id
    return names[0].name if names else self.id
    
def getSource(obj, type='source'):
    number = None
    volume = None
    year = None
    journal = None
    if isinstance(obj, Article):
        if hasattr(obj, 'number_id'):
            if obj.number_id is not None:
                number = obj.number_id
    if isinstance(obj, Number):
        number = obj
    if isinstance(obj, (Article, Number, Volume)):
        if number is not None:
            if hasattr(number, 'volume_id'):
                volume = number.volume_id
        elif isinstance(obj, Article):
            if hasattr(obj, 'volume_id'):
                volume = obj.volume_id
        else:
            volume = obj
    if isinstance(obj, (Article, Number, Volume, Year)):
        if hasattr(volume, 'year_id' ):
            if volume.year_id is not None:
                year = volume.year_id
        elif hasattr(number, 'year_id'):
            if number.year_id is not None:
                year = number.year_id
        else:
            year = obj
    if isinstance(obj, Journal):
        journal = obj
    elif isinstance(year, Year):
        if hasattr(year, 'journal_id'):
            journal  = year.journal_id
    
    if type == 'number':
        return number
    elif type == 'volume':
        return volume
    elif type == 'year':
        return year
    elif type == 'journal':
        return journal
    
    number = getName(number, NumberName)
    volume = getName(volume, VolumeName)
    year = getName(year, YearName)
    
    if isinstance(obj, Article):
        return (u'{0}, {1}, {2}, {3}').format(journal, year, volume, number)
    elif isinstance(obj, Number):
        nn = NumberName.objects.filter(par_id=obj.id)
        return (u'{0}, {1}, {2}, {3}').format(journal, year, volume, number)
    elif isinstance(obj, Volume):
        vn = VolumeName.objects.filter(id=obj.id)
        return (u'{0}, {1}, {2}').format(journal, year, volume)
    elif isinstance(obj, Year):
        yn = YearName.objects.filter(id=obj.id)
        return (u'{0}, {1}').format(journal, year)
    else:
        return (u'{0}').format(journal)

class AbstractMainObj(models.Model):
    def __unicode__(self):
        return self.source
        
    @property
    def source(self):
        return getSource(self)
        
    def sourceWithHier(self, type='source'):
        return getSource(self, type)
    
    @property    
    def getName(self):
        if isinstance(self, Article):
            an = ArticleName.objects.filter(par_id=self.id)
            return an[0]
        elif isinstance(self, Number):
            nn = NumberName.objects.filter(par_id=self.id)
            return nn[0]
        elif isinstance(self, Volume):
            vn = VolumeName.objects.filter(par_id=self.id)
            return vn[0]
        elif isinstance(self, Year):
            yn = YearName.objects.filter(par_id=self.id)
            return yn[0]
        else:
            return self
        
    class Meta:
        abstract = True
    
class AbstractDate(models.Model):
    def __unicode__(self):
        return (u'{0}  {1}').format(self.type, self.text)
        
    class Meta:
        abstract = True

class AbstractContributor(models.Model):
    def __unicode__(self):
        return u'{0} {1} {2}, {3}'.format(self.title, self.surname, self.firstname, self.title)
        
    class Meta:
        abstract = True

class AbstractDescription(models.Model):
    def __unicode__(self):
        return self.text

    class Meta:
        abstract = True

class AbstractKeywords(models.Model):
    def __unicode__(self):
        return self.kw
        
    class Meta:
        abstract = True

class AbstractName(models.Model):
    def __unicode__(self):
        return self.name
        
    class Meta:
        abstract = True

class AbstractReferences(models.Model):
    def __unicode__(self):
        return self.text

    class Meta:
        abstract = True

class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=2L)
    lang = models.CharField(max_length=255L)
    class Meta:
        db_table = 'language'
      
# extended clases

class JournalContributor(AbstractContributor):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Journal', db_column='par_id')
    parent = models.CharField(max_length=255L)
    role = models.CharField(max_length=255L, blank=True)
    title = models.CharField(max_length=255L, blank=True)
    surname = models.CharField(max_length=512L, blank=True)
    firstname = models.CharField(max_length=512L, blank=True)
    class Meta:
        db_table = 'journal_contributor'

class JournalDate(AbstractDate):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Journal', db_column='par_id')
    parent = models.CharField(max_length=255L, blank=True)
    type = models.CharField(max_length=255L, blank=True)
    text = models.TextField(blank=True)
    class Meta:
        db_table = 'journal_date'

class JournalName(AbstractName):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Journal', db_column='par_id')
    parent = models.CharField(max_length=255L)
    name = models.TextField(blank=True)
    lang = models.CharField(max_length=10L, blank=True)
    class Meta:
        db_table = 'journal_name'

class Journal(AbstractMainObj):
    def __unicode__(self):
        return getName(self, JournalName)
    #jid = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)
    legacy_id = models.CharField(max_length=255L, blank=True)
    parent = models.CharField(max_length=255L, blank=True)
    notes = models.TextField(blank=True)
    #id = models.CharField(max_length=255L, blank=True)
    issn = models.CharField(max_length=255L, blank=True)
    continuate = models.CharField(max_length=255L, blank=True)
    continuatedby = models.CharField(max_length=255L, db_column='continuatedBy', blank=True) # Field name made lowercase.
    frequency = models.CharField(max_length=255L, blank=True)
    www = models.CharField(max_length=255L, blank=True)
    czashum_promo = models.BooleanField()
    showCzashum = models.BooleanField(default=False, db_column=u'showCzashum')
    showPdf = models.BooleanField(default=False, db_column=u'showPdf')
    
    @property
    def getSecondName(self):
        qs = JournalName.objects.filter(par_id=self)
        if qs.count() > 1:
            return qs[1].name
        else:
            return ''
    
    @property
    def getContributor(self):
        if JournalContributor.objects.filter(par_id=self, role='publisher').exists():
            return (JournalContributor.objects.filter(par_id=self, role='publisher')[:1])[0].title
        else:
            return 1
    
    @property
    def getContributorId(self):
        if JournalContributor.objects.filter(par_id=self, role='publisher').exists():
            return (JournalContributor.objects.filter(par_id=self, role='publisher')[:1])[0].id
        else:
            return 1
    
    class Meta:
        db_table = 'journal'        

class YearContributor(AbstractContributor):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Year', db_column=u'par_id')
    parent = models.CharField(max_length=255L)
    role = models.CharField(max_length=255L, blank=True)
    title = models.CharField(max_length=255L, blank=True)
    surname = models.CharField(max_length=512L, blank=True)
    firstname = models.CharField(max_length=512L, blank=True)
    class Meta:
        db_table = 'year_contributor'
        
class Journalmap(models.Model):
    idjrl = models.ForeignKey('Journal', db_column=u'idjrl')
    iduser = models.ForeignKey(User, db_column=u'iduser')
    class Meta:
        db_table = 'journalMap'
        verbose_name = 'Journal Map'        

class YearDate(AbstractDate):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Year', db_column=u'par_id')
    parent = models.CharField(max_length=255L, blank=True)
    type = models.CharField(max_length=255L, blank=True)
    text = models.TextField(blank=True)
    class Meta:
        db_table = 'year_date'

class YearName(AbstractName):        
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Year', db_column=u'par_id')
    parent = models.CharField(max_length=255L)
    name = models.TextField(blank=True)
    lang = models.CharField(max_length=10L, blank=True)
    class Meta:
        db_table = 'year_name'

class Year(AbstractMainObj):        
    id = models.AutoField(primary_key=True)
    #journal_id = models.IntegerField(null=True, blank=True)
    journal_id = models.ForeignKey(Journal, db_column=u'journal_id')
    legacy_id = models.CharField(max_length=255L, blank=True)
    parent = models.CharField(max_length=255L, blank=True)
    notes = models.TextField(blank=True)
    class Meta:
        db_table = 'year'                

class VolumeContributor(AbstractContributor):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Volume', db_column='par_id')
    parent = models.CharField(max_length=255L)
    role = models.CharField(max_length=255L, blank=True)
    title = models.CharField(max_length=255L, blank=True)
    surname = models.CharField(max_length=512L, blank=True)
    firstname = models.CharField(max_length=512L, blank=True)
    class Meta:
        db_table = 'volume_contributor'

class VolumeName(AbstractName):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Volume', db_column='par_id')
    parent = models.CharField(max_length=255L)
    name = models.TextField(blank=True)
    lang = models.CharField(max_length=10L, blank=True)
    class Meta:
        db_table = 'volume_name'

class Volume(AbstractMainObj):
    id = models.AutoField(primary_key=True)
    #year_id = models.IntegerField(null=True, blank=True)
    year_id = models.ForeignKey(Year, db_column='year_id')
    legacy_id = models.CharField(max_length=255L, blank=True)
    parent = models.CharField(max_length=255L, blank=True)
    notes = models.TextField(blank=True)
    bibliographical_description = models.CharField(max_length=255L, blank=True)
    mht_typ_form = models.CharField(max_length=255L, blank=True)
    mht_typ_rodz = models.CharField(max_length=255L, blank=True)
    title_nonexplicit = models.TextField(blank=True)
    mph_reference = models.CharField(max_length=255L, blank=True)
    baztech_author_email = models.CharField(max_length=512L, blank=True)
    title = models.CharField(max_length=512L, blank=True)
    class Meta:
        db_table = 'volume'
        
    @property
    def isAccepted(self):
        if Dw.objects.filter(idvol=self.id, accepted = False):
            return ' *'
        else:
            return ''        

class NumberContributor(AbstractContributor):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Number', db_column=u'par_id')
    parent = models.CharField(max_length=255L)
    role = models.CharField(max_length=255L, blank=True)
    title = models.CharField(max_length=255L, blank=True)
    surname = models.CharField(max_length=512L, blank=True)
    firstname = models.CharField(max_length=512L, blank=True)
    class Meta:
        db_table = 'number_contributor'

class NumberName(AbstractName):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Number', db_column=u'par_id')
    parent = models.CharField(max_length=255L)
    name = models.TextField(blank=True)
    lang = models.CharField(max_length=10L, blank=True)
    
    @property
    def sortName(self):
        return self.name.split('-')[0]
    class Meta:
        db_table = 'number_name'
        
class Number(AbstractMainObj):
    id = models.AutoField(primary_key=True)
    #volume_id = models.IntegerField(null=True, blank=True)
    volume_id = models.ForeignKey(Volume, db_column='volume_id', blank=True, null=True)
    #year_id = models.IntegerField(null=True, blank=True)
    year_id = models.ForeignKey(Year, db_column='year_id', blank=True, null=True)
    legacy_id = models.CharField(max_length=255L, blank=True)
    parent = models.CharField(max_length=255L, blank=True)
    notes = models.TextField(blank=True)
    class Meta:
        db_table = 'number'
        
    @property
    def isAccepted(self):
        if Dw.objects.filter(idno=self.id, accepted = False):
            return ' *'
        else:
            return ''
        
class ArticleContributor(AbstractContributor):        
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Article', db_column=u'par_id')
    parent = models.CharField(max_length=255L)
    role = models.CharField(max_length=255L, blank=True)
    title = models.CharField(max_length=255L, blank=True)
    surname = models.CharField(max_length=512L, blank=True)
    firstname = models.CharField(max_length=512L, blank=True)
    
    def getCustomTitle(self):
        authTitle = ''
        if self.firstname:
            authTitle = self.firstname.strip()
        if self.surname:
            if self.firstname:
                authTitle += ' '
            authTitle += self.surname.strip()
        return authTitle
        
    @property
    def customTitleFiled(self):
        return self.getCustomTitle()
        
    class Meta:
        db_table = 'article_contributor'

class ArticleDate(AbstractDate):        
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Article', db_column=u'par_id')
    parent = models.CharField(max_length=255L, blank=True)
    type = models.CharField(max_length=255L, blank=True)
    text = models.TextField(blank=True)
    class Meta:
        db_table = 'article_date'

class ArticleDescription(AbstractDescription):        
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField()
    par_id = models.ForeignKey('Article', db_column=u'par_id')
    parent = models.CharField(max_length=255L, blank=True)
    lang = models.CharField(max_length=255L)
    text = models.TextField()
    class Meta:
        db_table = 'article_description'

class ArticleKeywords(AbstractKeywords):
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField()
    par_id = models.ForeignKey('Article', db_column=u'par_id')
    parent = models.CharField(max_length=255L, blank=True)
    lang = models.CharField(max_length=20L)
    kw = models.CharField(max_length=255L)
    class Meta:
        db_table = 'article_keywords'

class ArticleName(AbstractName): 
    def __unicode__(self):
        return self.name_clean
        
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Article', db_column=u'par_id')
    parent = models.CharField(max_length=255L)
    name = models.TextField(blank=True)
    name_clean = models.CharField(max_length=1500L, db_column='nameClean', blank=True)
    lang = models.CharField(max_length=10L, blank=True)
    class Meta:
        db_table = 'article_name'
        
class ArticlePages(models.Model):
    def __unicode__(self):
        if self.page_to == '':
            return self.page_from
        else:
            return self.page_from + '-' + self.page_to
        
    id = models.AutoField(primary_key=True)
    par_id = models.ForeignKey('Article', db_column=u'par_id')
    parent = models.CharField(max_length=255L, blank=True)
    page_from = models.CharField(max_length=255L, blank=True)
    page_to = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'article_pages'

class ArticleReferences(AbstractReferences):
    id = models.AutoField(primary_key=True, blank=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Article', db_column=u'par_id', blank=True, null=True)
    parent = models.CharField(max_length=255L, blank=True)
    index = models.CharField(max_length=20L, blank=True)
    text = models.TextField(blank=True)
    class Meta:
        db_table = 'article_references'

class ArticleReview(models.Model):
    def __unicode__(self):
        return self.full_name
#         return self.author + ', ' + self.title + ', ' + self.place + ' ' + self.year
    id = models.AutoField(primary_key=True)
    # par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Article', db_column=u'par_id', blank=True, null=True)
    parent = models.CharField(max_length=255L)
    title = models.CharField(max_length=255L, blank=True)
    author = models.CharField(max_length=255L, blank=True)
    place = models.CharField(max_length=512L, blank=True)
    year = models.CharField(max_length=512L, blank=True)
    full_name = models.CharField(max_length=2048L, blank=True)
    class Meta:
        db_table = 'article_review'
        
        
class Article(AbstractMainObj):
    def __unicode__(self):
        # return getName(self, ArticleName)
        return self.getName.name_clean
        
    id = models.AutoField(primary_key=True)
#     number_id = models.IntegerField(null=True, blank=True)
    number_id = models.ForeignKey(Number, db_column=u'number_id', null=True, blank=True)
#     volume_id = models.IntegerField(null=True, blank=True)
    volume_id = models.ForeignKey(Volume, db_column=u'volume_id', null=True, blank=True)
    legacy_id = models.CharField(max_length=255L, blank=True)
    parent = models.CharField(max_length=255L, blank=True)
    notes = models.TextField(blank=True)
    bibliographical_description = models.CharField(max_length=255L, blank=True)
    mht_typ_form = models.CharField(max_length=255L, blank=True)
    mht_typ_rodz = models.CharField(max_length=255L, blank=True)
    title_nonexplicit = models.TextField(blank=True)
    mph_reference = models.CharField(max_length=255L, blank=True)
    baztech_author_email = models.CharField(max_length=512L, blank=True)
    keywords = models.TextField(blank=True)
#     par_journal = models.ForeignKey(Journal, db_column=u'par_journal', null=True, blank=True)
#     par_year = models.ForeignKey(Year, db_column=u'par_year', null=True, blank=True)
#     par_volume = models.ForeignKey(Volume, db_column=u'par_volume', null=True, blank=True, related_name='par_volume')
    lang = models.CharField(max_length=255L, blank=True)
    
    @property
    def getAuthors(self):
        authors = ArticleContributor.objects.filter((Q(role='author') | Q(role='reviewed_work_author')|Q(role='translator')) & Q(par_id=self))
        return authors
        
    @property
    def getPages(self):
        pages = ArticlePages.objects.filter(par_id=self).order_by('id')
        return pages
    
    def getFirstPageSet(self):
        pages = ArticlePages.objects.filter(par_id=self).order_by('page_from')
        return pages[0] if pages else None
        
    @property
    def getLang(self):
        return (ArticleName.objects.filter(par_id=self.id))[0].lang
    
    class Meta:
        db_table = 'article'
        
class Hierarchy(models.Model):
    def __unicode__(self):
        return article
    
    id = models.IntegerField(primary_key=True)
    journal = models.ForeignKey(Journal, db_column=u'journal', null=True, blank=True)
    year = models.ForeignKey(Year, db_column=u'year', null=True, blank=True)
    volume = models.ForeignKey(Volume, db_column=u'volume', null=True, blank=True)
    number = models.ForeignKey(Number, db_column=u'number', null=True, blank=True)
    article = models.ForeignKey(Article, db_column=u'article', null=True, blank=True)
    # journal = models.IntegerField()
    # year = models.IntegerField()
    # volume = models.IntegerField()
    # number = models.IntegerField()
    # article = models.IntegerField()
    class Meta:
        db_table = 'hierarchy'

class Dw(models.Model):
    def __unicode__(self):
        return self.title1
    
    id = models.IntegerField(primary_key=True)
    title1 = models.CharField(max_length=1536L)
    title2 = models.CharField(max_length=1536L, blank=True)
    idno = models.ForeignKey(Number, db_column=u'idno', null=True, blank=True)
    number = models.CharField(max_length=512L, blank=True)
    idvol = models.ForeignKey(Volume, db_column=u'idvol', null=True, blank=True)
    volume = models.CharField(max_length=512L, blank=True)
    idyear = models.ForeignKey(Year, db_column=u'idyear', null=True, blank=True)
    year = models.CharField(max_length=128L)
    from_field = models.IntegerField(null=True, db_column='from', blank=True) #                                                                                         Field renamed because it was a Python reserved word.
    to = models.IntegerField(null=True, blank=True)
    idjrl = models.ForeignKey(Journal, db_column=u'idjrl', null=True, blank=True)
    journal = models.CharField(max_length=1024L)
    lang = models.CharField(max_length=5L)
    authors = models.CharField(max_length=2048L, blank=True, null=True)
    publisher = models.CharField(max_length=512, blank=True, null=True)
    accepted = models.BooleanField(default=False, db_column=u'accepted')
    showCzashum = models.BooleanField(default=False, db_column=u'showCzashum')
    showPdf = models.BooleanField(default=False, db_column=u'showPdf')
    fulltext = models.TextField(blank=True)
    
    class Meta:
        db_table = 'dw'
        
    def setAuthors(self):
        str = ""
        for a in self.getAuthors:
            if not str == '':
                str += ','
            str += a.getCustomTitle()
        self.authors = str
        self.save()
        return self.id
    
    def setPublishers(self):
        str = ''
        publishers = JournalContributor.objects.filter(par_id=self.idjrl,role='publisher')
        if publishers:
            self.publisher = publishers[0].title
            self.save()
        return self.id        
    
    @property
    def isNoAccepted(self):
        if Dw.objects.filter(idno=self.idno, accepted = False):
            return ' *'
        else:
            return ''
            
    @property
    def isVolAccepted(self):
        if Dw.objects.filter(idvol=self.idvol, accepted = False):
            return ' *'
        else:
            return ''
    
    @property
    def getAuthors(self):
        authors = ArticleContributor.objects.filter((Q(role='author') | Q(role='reviewed_work_author')|Q(role='translator')) & Q(par_id=self))
        return authors
        
    @property
    def getPages(self):
        pages = ArticlePages.objects.filter(par_id__id=self.id)
        return pages
     
    @property
    def getPagesString(self):
        pages = ArticlePages.objects.filter(par_id__id=self.id).order_by('page_from')
        resStr = ''
        if pages:
            resStr += 's. '
            for p in pages:
                if resStr == 's. ':
                    pass
                else:
                    resStr += ', ' 
                resStr += p.__unicode__()
        return resStr
    
    @property
    def getNameClean(self):
        if '/' in self.title1: 
            return self.title1.rpartition('/')[0]
        else:
            return self.title1
        
    def getSourceName(self):
        retStr = self.journal + ", " + self.year + ", "
        if self.volume:
            retStr += self.volume + ", "
        if self.number:
            retStr += self.number + ", "
        retStr += self.title1
        return retStr
    
#     @property
#     def getTxtCit(self):
#         articles = Article.objects.filter(id=self.id)
#         return exportTxt(articles, 'txt') 
#      
#     @property
#     def getBibCit(self):
#         articles = Article.objects.filter(id=self.id)
#         return exportTxt(articles, 'bibtex')
    
    @property
    def getFullTxt(self):
        from bib.util import prepNameForPath
        jrlDir = prepNameForPath(unicode(self.journal))
        if self.year != '' and self.year is not None:
            jrlDir += '-r' + prepNameForPath(unicode(self.year))
        jrlDir += '-t' + (prepNameForPath(unicode(self.volume)) if self.volume is not None else '')
        if self.number != '' and self.number is not None:
            jrlDir += '-n' + prepNameForPath(unicode(self.number))

        pages = self.getPages
        pageStr = ''
        if pages:
            page = pages[0]
            if page.page_to != '' and page.page_from != page.page_to:
                pageStr = '-s' + page.page_from + '-' + page.page_to
            else:
                pageStr = '-s' + page.page_from
        artDir = 'files/' + prepNameForPath(unicode(self.journal)) + '/' + jrlDir + '/' + jrlDir + pageStr        
        artPdf = artDir + '/' + jrlDir + pageStr + '.txt'
        return artPdf
    
    @property
    def getPdf(self):
        from bib.util import prepNameForPath
        jrlDir = prepNameForPath(unicode(self.journal))
        if self.year != '' and self.year is not None:
            jrlDir += '-r' + prepNameForPath(unicode(self.year))
        jrlDir += '-t' + (prepNameForPath(unicode(self.volume)) if self.volume is not None else '')
        if self.number != '' and self.number is not None:
            jrlDir += '-n' + prepNameForPath(unicode(self.number))

        pages = self.getPages
        pageStr = ''
        if pages:
            page = pages[0]
            if page.page_to != '' and page.page_from != page.page_to:
                pageStr = '-s' + page.page_from + '-' + page.page_to
            else:
                pageStr = '-s' + page.page_from
        artDir = 'files/' + prepNameForPath(unicode(self.journal)) + '/' + jrlDir + '/' + jrlDir + pageStr        
        artPdf = artDir + '/' + jrlDir + pageStr + '.pdf'
        return artPdf            

class FolderHierarchy(models.Model):
    def __unicode__(self):
        return self.name
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512L)
    parent = models.ForeignKey('FolderHierarchy', null=True, blank=True)
    user = models.ForeignKey(User, db_column=u'iduser')
    
    @property
    def getArticleCount(self):
        return Eshelf.objects.filter(parent=self).count()
    
class Eshelf(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article)
    parent = models.ForeignKey(FolderHierarchy, null=True, blank=True)
    user = models.ForeignKey(User, db_column=u'iduser')
    
class PasswordReset(models.Model):
    user = models.ForeignKey(User, db_column=u'iduser')
    password = models.CharField(max_length=512L)
    