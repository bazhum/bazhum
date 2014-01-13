function bindEvents() {
	$('.plus').unbind('click');
	$('.plus').click(addElem);
	$('.minus').unbind('click');
	$('.minus').click(remElem);
}

function renameInlines(tarElem) {
	var counterName = $($(tarElem).find('[name$=-counter]'))[0].name
    var nextCounterId = 0;
    
    $(document).find('[name='+counterName+']').parent().each(function() {    	
    	$(this).find('input').each(function() {    		
	    	if (this.name.match(/counter/) == null ) {    		
	    		this.name = this.name.replace(/-[0-9]+$/, '-' + nextCounterId);	    		
	    	}	    	
    	});
    	$(this).find('select').each(function() {    		    		
    		this.name = this.name.replace(/-[0-9]+$/, '-' + nextCounterId);	    		
    	});
    	nextCounterId++;
    });
}

function addElem(eve) {
	var tarElem = $(eve.target).parent().parent().parent().clone().insertAfter($(eve.target).parent().parent().parent());
    if(tarElem.find('.minus').length == 0) {
    	var minus = tarElem.find('.plus').after('<a href="#" class="minus button" title="">-</a>');
    }
    if (tarElem.find('span:contains("Tytuł:")').length > 0) {
    	tarElem.find('span:contains("Tytuł:")').html("Tytuł dzieła recenzowanego::");
    	tarElem.find('.select_wrap').hide('');
    }
    tarElem.find('[type="text"]').val('');
    tarElem.find('[type="hidden"]').val('');    
    tarElem.find('.error').html('');
    renameInlines(tarElem);
	bindEvents();
	return false;
}

function remElem(eve) {
	$(eve.target).parent().parent().parent().remove();
	renameInlines($(eve.target).parent().parent().parent());
	bindEvents();
	return false;
}

$(document).ready (function() {
	bindEvents();
	
	$( "#birds" ).autocomplete({
      source: "/bib/authorsSearch/",
      minLength: 2,
      select: function( event, ui ) {
        // log( ui.item ?
          // "Selected: " + ui.item.value + " aka " + ui.item.id :
          // "Nothing selected, input was " + this.value );
      }      
    });
});
