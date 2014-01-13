jQuery(document).ready(function($) {

    $("#eksportuj").click ( function() {
    	var idsDict = getIds();
        var ids = idsDict['ids'];
        var idsSec = idsDict['idsSec'];
        var idsType = idsDict['idsType'];
                    
        val = $('#format option:selected').text();
		if(val == 'Wybierz format')
		{
			alert('Musisz wybrać format eksportu');
			return false;
		}
		if($('input:checked[type=checkbox]').length == 0)
		{
			alert('Musisz zaznaczyć rekordy do eksportu');
			return false;
		}		
		
        window.location.href = "/bib/export/?type="+$('#format').val()+"&ids=" + ids + "&idsType=" + idsType + "&idsSec=" + idsSec;
        return false;
    });
    
    $('#eshelf_add').click (function() {
    	var idsDict = getIds();
        var ids = idsDict['ids'];
        var idsSec = idsDict['idsSec'];
        var idsType = idsDict['idsType'];
        var vars = 'type=eshelf_add&idsType='+idsType+'&ids='+ids+'&idsSec='+idsSec;
        
        $.ajax({
		type: "get",
		url: '/bib/ajax/?' + vars,
		cache: false,				
		// data: getDict,
        data: {},
		success: function(response){			
			try{
                if (response != '')
                	$('#eshelf_count').text(response);
                    alert('Pomyślnie dodano rekordy do e-półki.');
			}catch(e) {		
				alert('Exception while request..');
			}		
		},
		error: function(){						
			// alert('Error while request..');
		}
	 });
	 return false;
    });
    
    $('#checkboxMain').change ( function(event) {
        if ($(event.target).prop('checked'))
            $('.check').attr('checked', true);
        else
            $('.check').attr('checked', false);
    });
	
});