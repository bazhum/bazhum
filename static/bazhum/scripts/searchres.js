var morePressed = function (event) {
    curCount = parseInt($(event.target).attr('count'));
    if (isNaN(curCount)) {
        $(event.target).attr('count', 9);
        curCount = 9;
        $(event.target).parent().prev().find('li:lt('+curCount+')').show();
    } else {
        curCount += 5;
        $(event.target).attr('count', curCount);
        $(event.target).parent().prev().find('li:lt('+curCount+')').show();
    }
    if ($(event.target).parent().prev().children().length <= curCount)
            $(event.target).parent().remove();
    return false;
}

var processing = false;

function loadData() {
	page = parseInt($('.table_content').attr('pageNo'));
	$('.table_content').attr('pageNo', page+1);
    
    url = window.location.href;
//    vars = url.split('?')[1].split('&');
    vars = url.split('?')[1];
    // getDict = {};
    // for (c in vars) {
        // getVar = vars[c].split('=');
        // getDict[getVar[0]] = decodeURIComponent(getVar[1]);
    // }
    
    vars += '&pageNo='+(page+1)+'&type=results';
    // getDict['pageNo'] = page+1;
    // getDict['type'] = 'results';

	$.ajax({
		type: "get",
		url: '/bib/ajax/?' + vars,
		cache: false,				
		// data: getDict,
        data: {},
		success: function(response){			
			try{
                if (response != '')
                    $('.table_content').append(response)
                    processing = false;
			}catch(e) {		
				alert('Exception while request..');
			}		
		},
		error: function(){						
			// alert('Error while request..');
		}
	 });
	

}

jQuery(document).ready(function($) {
    processing = false;

	if ($('#filter_journals').children().length <= 5)
        $('#more_journal').remove();
    else 
        $('#filter_journals li:gt(4)').hide();
    
    if ($('#filter_authors').children().length <= 5)
        $('#more_auth').remove();
    else 
        $('#filter_authors li:gt(4)').hide();
    
    if ($('#filter_lang').children().length <= 5)
        $('#more_lang').remove();
    else 
        $('#filter_lang li:gt(4)').hide();
        
    $('.more').click(morePressed);
    
    $('#zawezOkres').click (function() {
        window.location.href = window.location.href + "&dateRange=1&fFrom=" + $('#fFrom').val() + "&fTo=" + $('#fTo').val();
        return false;
    });
	
	$(window).scroll(function () {     
        if (processing == true)
            return false;
        if ($(window).scrollTop() >= ( $(document).height() - $(window).height()-1000)) {
            processing = true;
            loadData();
        }
    });

    
    
});