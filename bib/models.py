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

# base clases & func

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
        #return (u'{0}, {1}, {2}, {3}').format(journal, year, volume, nn[0].name)
        return (u'{0}, {1}, {2}, {3}').format(journal, year, volume, number)
    elif isinstance(obj, Volume):
        vn = VolumeName.objects.filter(id=obj.id)
        #return (u'{0}, {1}, {2}').format(journal, year, vn[0].name)
        return (u'{0}, {1}, {2}').format(journal, year, volume)
    elif isinstance(obj, Year):
        yn = YearName.objects.filter(id=obj.id)
        #return (u'{0}, {1}').format(journal, yn[0].name)
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
    
    @property
    def getSecondName(self):
        qs = JournalName.objects.filter(par_id=self)
        if qs.count() > 1:
            return qs[1].name
        else:
            return ''
    
    @property
    def getContributor(self):
        return (JournalContributor.objects.filter(par_id=self)[:1])[0].title
    
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
        
class ArticleContributor(AbstractContributor):        
    id = models.AutoField(primary_key=True)
    #par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Article', db_column=u'par_id')
    parent = models.CharField(max_length=255L)
    role = models.CharField(max_length=255L, blank=True)
    title = models.CharField(max_length=255L, blank=True)
    surname = models.CharField(max_length=512L, blank=True)
    firstname = models.CharField(max_length=512L, blank=True)
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
        
    id = models.IntegerField(primary_key=True)
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
        return self.title
    id = models.IntegerField(primary_key=True)
    # par_id = models.IntegerField(null=True, blank=True)
    par_id = models.ForeignKey('Article', db_column=u'par_id', blank=True, null=True)
    parent = models.CharField(max_length=255L)
    title = models.CharField(max_length=255L, blank=True)
    author = models.CharField(max_length=255L, blank=True)
    place = models.CharField(max_length=512L, blank=True)
    year = models.CharField(max_length=512L, blank=True)
    class Meta:
        db_table = 'article_review'
        
        
class Article(AbstractMainObj):
    def __unicode__(self):
        return getName(self, ArticleName)
        
    id = models.AutoField(primary_key=True)
    #number_id = models.IntegerField(null=True, blank=True)
    number_id = models.ForeignKey(Number, db_column=u'number_id', null=True, blank=True)
    #volume_id = models.IntegerField(null=True, blank=True)
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
    
    @property
    def getAuthors(self):
        authors = ArticleContributor.objects.filter(role='author', par_id=self)
        # authorsStr = ','.join([x.title for x in authors])
        # if authors.count() == 0:
            # name = (ArticleName.objects.filter(par_id=self))[0].name
            # if name.rsplit("/",1).__len__() == 2:
                # authorsStr = name.rsplit("/",1)[1]
                # authors
        return authors
    
    class Meta:
        db_table = 'article'