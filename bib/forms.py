# -*- coding: utf-8 -*-
from django.forms import *
from django.conf import settings
from django.contrib.auth.models import User

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
    
class JournalMapForm(baseForm):
    idjrl = AjaxForeignKeyField(Journal, baseForm.lookups)
    iduser = AjaxForeignKeyField(User, baseForm.lookups)
    
class registrationForm(forms.Form):
    username = CharField(required=True, max_length=255, widget=TextInput(attrs={'required':''}))
    email = EmailField(required=True, max_length=255, widget=TextInput(attrs={'required':''}))
    password = CharField(required=True,widget=PasswordInput(attrs={'required':''}))
    password2 = CharField(required=True,widget=PasswordInput(attrs={'required':''}))
    
class loginForm(forms.Form):
    username = CharField(required=True, max_length=255, widget=TextInput(attrs={'required':''}))
    password = CharField(required=True,widget=PasswordInput(attrs={'required':''}))
    
class passwordResetForm(forms.Form):
    username = EmailField(required=True, max_length=255, widget=TextInput(attrs={'required':''}))
    password = CharField(required=True,widget=PasswordInput(attrs={'required':''}))
    password2 = CharField(required=True,widget=PasswordInput(attrs={'required':''}))
    
    def clean(self):
        cleaned_data = super(passwordResetForm, self).clean()
        pass1 = cleaned_data.get("password")
        pass2 = cleaned_data.get("password2")
        if pass1 and pass2:
            if pass1 != pass2:
                raise forms.ValidationError("Hasła muszą być identyczne.")

        # Always return the full collection of cleaned data.
        return cleaned_data