var morePressed = function (event) {
    curCount = parseInt($(event.target).attr('count'));
    if (isNaN(curCount)) {
        $(event.target).attr('count', 9);
        curCount = 9;
        $(event.target).parent().prev().find('li:lt('+curCount+')').slideDown();
    } else {
        curCount += 5;
        $(event.target).attr('count', curCount);
        $(event.target).parent().prev().find('li:lt('+curCount+')').slideDown();
    }
    if ($(event.target).parent().prev().children().length <= curCount)
            $(event.target).parent().remove();
    return false;
}

jQuery(document).ready(function($) {

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
        $('#filter_authors li:gt(4)').hide();
        
    $('.more').click(morePressed);
    
    $('#zawezOkres').click (function() {
        window.location.href = window.location.href + "&dateRange=1&fFrom=" + $('#fFrom').val() + "&fTo=" + $('#fTo').val();
        return false;
    });
    
});