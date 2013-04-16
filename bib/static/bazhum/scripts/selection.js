jQuery(document).ready(function($) {

    $("#eksportuj").click ( function() {
        var ids = new Array();
        var idsSec = new Array();
        $('.check').each ( function() {
            if (window.location.href.indexOf("bib/volume/") > -1) {
                if ($(this).prop('checked')) {
                    if ($(this).attr('name') == 'checkboxN')
                        idsSec.push($(this).val());
                    else
                        ids.push ($(this).val());
                    }
            } else ($(this).attr('name') == 'checkboxA')
                if ($(this).prop('checked')) {
                    ids.push ($(this).val());
                }
        });
        
        if (window.location.href.indexOf("bib/article/") > -1) {
            ids.push($(this).attr('article'));   
        }
            
        var idsType='';
        if(window.location.href.indexOf("bib/journal/") > -1) {
            idsType='vol';
        } else if(window.location.href.indexOf("bib/volume/") > -1) {
            idsType='num_art';
        }
        
        window.location.href = "/bib/export/?type="+$('#format').val()+"&ids=" + ids + "&idsType=" + idsType + "&idsSec=" + idsSec;
        return false;
    });

    $('#checkboxMain').change ( function(event) {
        if ($(event.target).prop('checked'))
            $('.check').attr('checked', true);
        else
            $('.check').attr('checked', false);
    });
	
});