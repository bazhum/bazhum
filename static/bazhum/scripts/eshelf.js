function makeDroppable() {
	$(".folders li").droppable({
  	greedy: true,
    tolerance: 'pointer',
    drop: function(event, ui) {
        var id = ($(this))[0].id;
        
        var statusDrag = ui.draggable.find('.check').attr('checked');
        
        if (statusDrag != 'checked')
        {
	        var sourceId = ui.draggable.find('a').attr('href').match(/[0-9]+/);  
	        var vars = 'type=article_move&idDir=' + id + '&idArt=' + sourceId;
	        
	        $.ajax({
				type: "get",
				url: '/bib/ajax/?' + vars,
				cache: false,				
				success: function(response){			
					// try{
		                if (response != '')
		                {
		                	var obFolder = null;
		                	if (id != '')
		                		obFolder = $('#'+id+' a'); 
	                		else
		                		obFolder = $(($('.rootFolder a'))[0]);
		                		
		                	if (obFolder.html().match(/\([0-9]+\)/) == null )
		                		obFolder.append(' (1)');
	                		else {
	                			var count = (obFolder.html().match(/\([0-9]+\)/))[0];
	                			count = count.replace('(', '').replace(')', '');
	                			count = parseInt(count) + 1;
	                			obFolder.html(obFolder.html().replace(/\([0-9]+\)/, '('+count+')'));                			
	                		}
	                		var currCntObj = null;
	                		if ($('.folders .active a').length != 0)
	                			currCntObj = $('.folders .active a');
	            			else
	            				currCntObj = $('.folders a.active');
	            				
	        				var curCnt = (currCntObj.html().match(/\([0-9]+\)/))[0];
	            			curCnt = parseInt(curCnt.replace('(', '').replace(')', ''));                			
	            			if (curCnt == 1) {
	            				currCntObj.html(currCntObj.html().replace(/\([0-9]+\)/, ''));
	            			}
	            			else {
	            				currCntObj.html(currCntObj.html().replace(/\([0-9]+\)/, '('+(curCnt-1)+')'));
	            			}
		                    $('[value='+sourceId+'].check').parent().parent().parent().remove();
	                    }
					// }catch(e) {		
						// alert('Exception while request..');
					// }		
				}
		 	});	
	    	ui.draggable.remove();
        }
        var ids = getIds()['ids'];

        for (var i = 0; i < ids.length; i++)
        {
	        //var sourceId = ui.draggable.find('a').attr('href').match(/[0-9]+/);
	        var selId = ids[i];
	        
	        var vars = 'type=article_move&idDir=' + id + '&idArt=' + selId;
	        
	        $.ajax({
				type: "get",
				url: '/bib/ajax/?' + vars,
				cache: false,				
				success: function(response){			
					// try{
		                if (response != '')
		                {
		                	var obFolder = null;
		                	if (id != '')
		                		obFolder = $('#'+id+' a'); 
	                		else
		                		obFolder = $(($('.rootFolder a'))[0]);
		                		
		                	if (obFolder.html().match(/\([0-9]+\)/) == null )
		                		obFolder.append(' (1)');
	                		else {
	                			var count = (obFolder.html().match(/\([0-9]+\)/))[0];
	                			count = count.replace('(', '').replace(')', '');
	                			count = parseInt(count) + 1;
	                			obFolder.html(obFolder.html().replace(/\([0-9]+\)/, '('+count+')'));                			
	                		}
	                		var currCntObj = null;
	                		if ($('.folders .active a').length != 0)
	                			currCntObj = $('.folders .active a');
	            			else
	            				currCntObj = $('.folders a.active');
	            				
	        				var curCnt = (currCntObj.html().match(/\([0-9]+\)/))[0];
	            			curCnt = parseInt(curCnt.replace('(', '').replace(')', ''));                			
	            			if (curCnt == 1) {
	            				currCntObj.html(currCntObj.html().replace(/\([0-9]+\)/, ''));
	            			}
	            			else {
	            				currCntObj.html(currCntObj.html().replace(/\([0-9]+\)/, '('+(curCnt-1)+')'));
	            			}
	            			
		                    $('[value='+response+'].check').parent().parent().parent().remove();
	                    }
					// }catch(e) {		
						// alert('Exception while request..');
					// }		
				}
		 	});		 	
    	}
    	
    	//alert('Pomyślnie przeniesiono artykuł do innego folderu.');
    }
  });
}

$(document).ready(function (){
  $(".add_new").click(function(){
  	$('.popup_window h2').text(gettext('Podaj nazwę nowego folderu:'));
  	$('.buttons_wrap').html('<input id="addBtn" type="submit" name="" value="'+gettext('Zatwierdź')+'">');
  	$('.popup_content').show();
  	$('.eshelf_popup').show();
  	$('#addBtn').click(function() {
  		var name = $('#folderData').val();
  		var vars = 'type=folder_add&name=' + name;
        
        $.ajax({
			type: "get",
			url: '/bib/ajax/?' + vars,
			cache: false,				
			success: function(response){			
				try{
	                if (response != '')
	                {
	                	$('#folders').append('<li id="'+response+'"><a href="">'+name+'</a></li>');
	                    //alert('Pomyślnie dodano nowy folder.');
	                    makeDroppable();
	                    $(".popup").hide();
                    }
				}catch(e) {		
					alert('Exception while request..');
				}		
			}
	 	});
  		return false;
  	});
    $(".eshelf_popup").show();
  });
  
  $("#rename_folder").click(function(){
  	if ($('.folders .active').length == 0) {
  		alert(gettext('Musisz zaznaczyć folder do zmiany nazwy.'));
		return false;
	}
  	$('.popup_window h2').text(gettext('Czy na pewno zmienić nazwę folderu?'));
  	$('.popup_content').show();
  	$('.buttons_wrap').html('<input id="renameBtn" type="submit" name="" value="'+gettext('Zatwierdź')+'">');
  	$('.eshelf_popup').show();  
  	$('#renameBtn').click(function() {	  		
  		var id = ($('.folders .active'))[0].id;
  		var name = $('#folderData').val();
  		var vars = 'type=folder_rename&id=' + id + '&name=' + name;
        
        $.ajax({
			type: "get",
			url: '/bib/ajax/?' + vars,
			cache: false,				
			success: function(response){			
				try{
	                if (response != '')
	                {
	                	currCntObj = null;
	                	if ($('.folders .active a').length != 0)
                			currCntObj = $('.folders .active a');
            			else
            				currCntObj = $('.folders a.active');
            				
        				var curCnt = (currCntObj.html().match(/\([0-9]+\)/))[0];
	                	$('#'+id+'.active').replaceWith('<li id="'+id+'" class="active"><a href="">'+name+' '+curCnt+'</a></li>');
	                    //alert('Pomyślnie zmieniono nazwę.');
	                    $(".popup").hide();
                    }
				}catch(e) {		
					alert('Exception while request..');
				}		
			}
	 	});
  		return false;
  	});
    $(".eshelf_popup").show();
  });
  
  $("#empty_folder").click(function(){
  	$('.popup_window h2').text(gettext('Czy na pewno opróżnić folder?'));
  	$('.buttons_wrap').html('<input id="renameBtn" type="submit" name="" value="'+gettext('Zatwierdź')+'">');
  	$('.popup_content').hide();
  	$('.eshelf_popup').show();  
  	$('#renameBtn').click(function() {	  		
  		var id = 0;
  		if (($('.folders .active'))[0].id != "")
  			id = ($('.folders .active'))[0].id;
  		var vars = 'type=folder_empty&id=' + id;
        
        $.ajax({
			type: "get",
			url: '/bib/ajax/?' + vars,
			cache: false,				
			success: function(response){			
				try{
	                if (response != '')
	                {
	                	$('.table_content').remove();	                	
	                    $(".popup").hide();
                    }
				}catch(e) {		
					alert('Exception while request..');
				}		
			}
	 	});
  		return false;
  	});
    $(".eshelf_popup").show();
  });
  
  $("#eshelf_del").click(function() {
  	// var currCntObj = null;
  	// var id = '';
	// if ($('.folders .active a').length != 0)
		// currCntObj = $('.folders .active a');
		// id = ($('.folders .active a'))[0].href.match(/e_shelf\/([0-9]+)/)[0].match(/[0-9]+/)[0]
	// else
		// currCntObj = $('.folders a.active');
	
		
  	var ids = getIds()['ids'];
    for (var i = 0; i < ids.length; i++)
    {
        //var sourceId = ui.draggable.find('a').attr('href').match(/[0-9]+/);
        var selId = ids[i];
        
        var vars = 'type=article_del&idArt=' + selId;
        
        $.ajax({
			type: "get",
			url: '/bib/ajax/?' + vars,
			cache: false,				
			success: function(response){			
				// try{
	                if (response != '')
	                {
	                	// var obFolder = null;
	                	// if (id != '')
	                		// obFolder = $('#'+id+' a'); 
                		// else
	                		// obFolder = $(($('.rootFolder a'))[0]);
	                		
                		var currCntObj = null;
                		if ($('.folders .active a').length != 0)
                			currCntObj = $('.folders .active a');
            			else
            				currCntObj = $('.folders a.active');
            				
        				var curCnt = (currCntObj.html().match(/\([0-9]+\)/))[0];
            			curCnt = parseInt(curCnt.replace('(', '').replace(')', ''));                			
            			if (curCnt == 1) {
            				currCntObj.html(currCntObj.html().replace(/\([0-9]+\)/, ''));
            			}
            			else {
            				currCntObj.html(currCntObj.html().replace(/\([0-9]+\)/, '('+(curCnt-1)+')'));
            			}
            			
	                    $('[value='+response+'].check').parent().parent().parent().remove();
                    }
				// }catch(e) {		
					// alert('Exception while request..');
				// }		
			}
	 	});		 	
	}
  });

  $("#del_folder").click(function(){
  	if ($('.folders .active').length == 0) {
  		alert('Musisz zaznaczyć folder do usunięcia.');
		return false;
	}
  	$('.popup_window h2').text(gettext('Czy na pewno chcesz usunąć folder?'));
  	$('.buttons_wrap').html('<input id="delYesBtn" type="submit" name="" value="'+gettext('Tak')+'"><input id="delNoBtn" class="secondary_button" type="submit" name="" value="'+gettext('Nie')+'">');
  	$('#delNoBtn').click(function() {
  		$(".popup").hide();
  		return false;
  	});
  	$('#delYesBtn').click(function() {	
  		var id = ($('.folders .active'))[0].id;
  		var vars = 'type=folder_del&id=' + id;
        
        $.ajax({
			type: "get",
			url: '/bib/ajax/?' + vars,
			cache: false,				
			success: function(response){			
				try{
	                if (response != '')
	                {
	                	$('#'+id+'.active').remove();
	                    alert('Pomyślnie usunięto folder.');
	                    $(".popup").hide();
	                    $('.table_content.full_width').children().hide();
	                    $('.pagination').hide();
                    }
				}catch(e) {		
					alert('Exception while request..');
				}		
			}
	 	});
  		return false;
  	});
  	$('.popup_content').hide();
    $(".eshelf_popup").show();
  });

  $(".popup_closer, .popup_overlay").click(function(){
    $(".popup").hide();
  });
  
  $(".line").draggable({
  		revert: true
    });
  
  makeDroppable();
});
