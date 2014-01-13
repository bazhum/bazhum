var typeField = '<span class="label_select" id="div_f"> \
                           <span class="select_wrap"> \
                            <select name="typeField" id="typeField"> \
                              <option selected value="any">Dowolne pole</option> \
                              <option value="title">Tytuł</option> \
                              <option value="author">Autor</option> \
                              <option value="jrl">Tytuł czasopisma</option> \
                              <option value="date">Data wydania</option> \
                              <option value="lang">Język</option> \
                            </select> \
                          </span> \
                        </span>';
var textField = '<span class="search_column" id="div_sc"> \
	  <span class="plus_minus"> \
		<!-- <a href="#" class="minus button" title="">-</a> --> \
		<a href="#" class="plus button" id="pb" title="">+</a> \
		<a href="#" class="minus button" id="mb" title="">-</a> \
	  </span> \
	  <span class="input_wrap"> <input autocomplete="off" type="text" name="valueField" id="valueField" value="" placeholder="" /></span> \
	</span>';
var yearField = '<span class="search_column" id="div_sc"> \
	  <span class="plus_minus"> \
		<a href="#" class="plus button" id="pb" title="">+</a> \
		<a href="#" class="minus button" id="mb" title="">-</a> \
	  </span> \
	  <span class="input_wrap year"> \
		Od roku&nbsp;&nbsp;<input type="text" name="valueField" id="valueField" value="" placeholder="">&nbsp;&nbsp;do&nbsp;&nbsp; \
		<input autocomplete="off" type="text" name="valueField" id="valueField" value="" placeholder=""> \
	  </span> \
	</span>';
var listField = '<span class="search_column" id="div_sc"> \
	  <span class="plus_minus"> \
		<a href="#" class="plus button" id="pb" title="">+</a> \
		<a href="#" class="minus button" id="mb" title="">-</a> \
	  </span> \
	  <span class="input_wrap"> \
		<span class="select_wrap"> \
		  <select autocomplete="off" name="valueField" id="valueField"> \
			  #lang# \
			</select> \
		</span> \
	  </span> \
	</span>';

var prev = '';
    
var plusEvFunc = function(event) {
	fieldCount = parseInt($('#fieldCnt').val());
	if (fieldCount < 5) {
		lastRow = $('#search_elements_conteiner li:last-child');
		// ft = typeField.replace(/##/g, fieldCount+1);
		// fi = textField.replace(/##/g, fieldCount+1);
		ft = typeField.replace(/##/g, '');
		fi = textField.replace(/##/g, '');
		lastRow.after('<li>'+ft+fi+'</li>');
		rebindControlos();
		$('#fieldCnt').val(fieldCount+1);
	}	
	return false;
}

var minEvFunc = function(event) {
	$(event.target).parent().parent().parent().remove();
	$('#fieldCnt').val(parseInt($('#fieldCnt').val())-1);
	return false;
}

var changeSearchType = function(event) {
	type = $(event.target).find(':selected').text();
	fieldContainer = $(event.target).parent().parent().parent();
//    alert(prev);
    if (prev != 'lang' && prev != 'date')
        prevVal = fieldContainer.children().last().find('#valueField').val();
    else
        prevVal = '';
	fieldContainer.children(':last-child').remove();
	
	if (type == 'Data wydania') {
		fieldContainer.children(':last-child').after(yearField);
	} else if (type == 'Język') {
		fieldContainer.children(':last-child').after(listField.replace('#lang#', $('#langs').html()));
	} else {
		fieldContainer.children(':last-child').after(textField);
        fieldContainer.children().last().find('#valueField').val(prevVal);
	}
	
	if (fieldContainer.index() == 0)
			fieldContainer.children(':last-child').find('.minus').remove();
	
}

function rebindControlos() {
	$('.plus').unbind();
	$('.minus').unbind();
	$('.plus').click(plusEvFunc);
	$('.minus').click(minEvFunc);
	$('.label_select select').unbind();
	$('.label_select select').focus(function() {
        sel = $(event.target);
        prev=sel.val();
        }).change(changeSearchType);
}
	
jQuery(document).ready(function($) {

	rebindControlos()
	
});