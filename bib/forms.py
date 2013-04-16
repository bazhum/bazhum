# -*- coding: utf-8 -*-
from django.forms import *
from django.conf import settings
from ajax_filtered_fields.forms import *

from bib.models import *

class baseForm(ModelForm):
    lookups = (
            ('all stuff', {}),
        )
        
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
            settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js",
            '/static/jquery-1.9.1.min.js',
            '/static/js/ajax_filtered_fields.js',
        )

class NumberForm(baseForm): 
    volume_id = AjaxForeignKeyField(Volume, baseForm.lookups)
    year_id = AjaxForeignKeyField(Year, baseForm.lookups)
    
class ArticleForm(baseForm): 
    volume_id = AjaxForeignKeyField(Volume, baseForm.lookups)
    number_id = AjaxForeignKeyField(Number, baseForm.lookups)
    
class VolumeForm(baseForm): 
    year_id = AjaxForeignKeyField(Year, baseForm.lookups)    
    
class YearForm(baseForm): 
    journal_id = AjaxForeignKeyField(Journal, baseForm.lookups)    