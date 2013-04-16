# -*- coding: utf-8 -*-

from ajax_filtered_fields.forms import *
from django import forms
from django.forms.util import ValidationError
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from ajax_filtered_fields.forms import FilteredSelectMultiple, FilteredSelect
from ajax_filtered_fields import utils

class widget_fs_mod(FilteredSelect):
    def render(self, name, value, attrs=None, choices=()):
        self._element_id = attrs['id']
        # choices links
        # if there is only one choice, then nothing will be rendered
        lookups_output = ""
        lookups = utils.getLookups(self.lookups)
        if len(lookups) > 1:
            js_method_name = "getForeignKeyJSON"
            lookups_output = "\n".join(
                _renderFilter(js_method_name, self._element_id, 
                    self.model, i, self.select_related) 
                for i in lookups)
                
        # get the selected object name
        selection = "-" * 9
        if value:
            selection = utils.getObject(self.model, {"pk": value}, 
                self.select_related)
        
        # filter selectbox input
        filter_id = "%s_input" % self._element_id
        
        # give a style to the final select widget
        _attrs = {"size": 2, "style": "width:670px;"}
        try:
            attrs.update(_attrs)
        except AttributeError:
            attrs = _attrs
            
        # normal widget output from the anchestor
        # create a field with a dummy name , the real value
        # will be retrieved from a hidden field
        parent_output = super(FilteredSelect, self
            ).render("dummy-%s" % name, value, attrs, choices)
        
        # output
        mapping = {
            "lookups_output": lookups_output,
            "selection": selection,
            "filter_id": filter_id,
            "parent_output": parent_output,
            "name": name,
            "element_id": self._element_id, 
            "value": "" if value is None else value,
            }
                            
        output = u"""
            <div class="selector">
                %(lookups_output)s
            </div>
            
            <div class="selector">
                <div class="selector-available">
                    <h2>%(selection)s</h2>
                    <p class="selector-filter">
                        <img src="/media/img/admin/selector-search.gif"> 
                        <input id="%(filter_id)s" type="text">
                    </p>
                    %(parent_output)s
                </div>
            </div>
            
            <input type="hidden" name="%(name)s" id="hidden-%(element_id)s" value="%(value)s" />
            
            <script type="text/javascript" charset="utf-8">
        		$(document).ready(function(){
                    SelectBox.init('%(element_id)s');

                    $("#%(filter_id)s").bind("keyup", function(e) {
                        SelectBox.filter("%(element_id)s", $("#%(filter_id)s").val())
                    });
                    
                    $(".ajax_letter").click(function(e) {
                        $("#%(filter_id)s").val("");
                    });
                    
                    ajax_filtered_fields.bindForeignKeyOptions("%(element_id)s");
        		});
        	</script>
            """ % mapping
            
        return mark_safe(output)

        

class aff_mod(AjaxForeignKeyField):
    def __init__(self, model, lookups, qs, default_index=0, select_related=None,
        widget=widget_fs_mod, *args, **kwargs):
        """
        See the AjaxManyToManyField docstring.
        """
        # get the default index and queryset
        # queryset is empty if default index is None
        if default_index is None:
            queryset = model.objects.none()
        else:
            lookups_list = utils.getLookups(lookups)
            lookup_dict = lookups_list[default_index][1]
            # get the queryset
            queryset = utils.getObjects(model, lookup_dict, select_related)
        # call the parent constructor
        super(AjaxForeignKeyField, self
            ).__init__(qs, widget=widget, *args, **kwargs)
        # populate widget with some data
        self.widget.lookups = self.lookups = lookups
        self.widget.model = self.model = model
        self.widget.select_related = select_related