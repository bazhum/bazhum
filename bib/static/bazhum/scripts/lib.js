function getIds() {
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
        ids.push($('#eksportuj').attr('article'));   
    }
    
    var idsType='';
    if(window.location.href.indexOf("bib/journal/") > -1) {
        idsType='vol';
    } else if(window.location.href.indexOf("bib/volume/") > -1) {
        idsType='num_art';
    } else if(window.location.href.indexOf("bib/list/publisher/") > -1) {
        idsType='journal';
    }
    
    return {'ids': ids, 'idsSec': idsSec, 'idsType': idsType}
}


function getId (val) {
	val = val.replace(/\D/g,'');
	return val;
}

function validateEmail(emailaddress){  
   var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;  
   if(!emailReg.test(emailaddress)) {  
        return true;
   }
   return false;       
}

$(document).ready(function() {
  $(".popup_closer, .popup_overlay").click(function(){
    $(".popup").hide();
  });

  $(".login_link").click(function(){
    $(".login_popup").show();
  });

  $(".register_link").click(function(){
    $(".register_popup").show();
  });
  
  $("#create_account").click(function() {
  	var isValid = true;
  	if (validateEmail($('[name=email]').val())) {
  		$('.error_comment.email').text('Niepoprawny adres email.');
  		isValid = false;
  	}
  	else {
  		$('.error_comment.email').text('');
  	}  		
  	if ($('[name=username]').val() == '') {
  		$('.error_comment.name').text('Nazwa użytkownika nie może być pusta.');
  		isValid = false;
  	}  		
  	else {
  		$('.error_comment.name').text('');
	}  		
  		
	if ($('[name=password]').val() != $('[name=password2]').val()) {
		$('.error_comment.pass').text('Hasła muszą sie zgadzać.');
		isValid = false;
	}
	else {
		$('.error_comment.pass').text('');
	}
	if ($('[name=password]').val() == '') {
		$('.error_comment.pass').text('Hasło nie może być puste.');
		isValid = false;
	}
	else {
		$('.error_comment.pass').text('');
	}
				
	if (isValid) {
		$('#register_form').submit();		
	}
	return false;
  });
  
  $('#popupLogowanie').click(function() {
  	$(".popup").hide();
  	$(".login_popup").show();
  });
});
  