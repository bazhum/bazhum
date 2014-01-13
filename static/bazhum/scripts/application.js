jQuery(document).ready(function($) {
  
  function gridShow(){
  $("#main_conteiner").gridPreview({
      'columns':12,
      'columnClass': 'grid_1',
      'line': 24,
      'modul': 2,
      'topOffset': 0,
      'leftOffset': 24,
      'toggleGrid': 'g', 
      'toggleZindex': 'f',
      'showAtStart': false,
      'showOnTop': true
    });
  }
    gridShow();

  $(window).resize(function(){
    $("#gridPreviewHolder").remove();
    gridShow();
  });

  // Start your functions here

  $("#content_conteiner").css({"padding-bottom": $("#footer").outerHeight()});

  var menuOpened = false;
  
  $("#menu_box_icon").click(function(){
    if(!menuOpened){
      $("#menu_box").show();
      menuOpened = true;
    }
    else{
      $("#menu_box").hide();
      menuOpened = false
    }
  })

  var editMenuOpened = false;
  
  $(".edit_folder span").click(function(){
    if(!editMenuOpened){
      $(".edit_menu").show();
      editMenuOpened = true;
    }
    else{
      $(".edit_menu").hide();
      editMenuOpened = false
    }
  })

  $(document).click(function(e){
    if($(e.target).closest('.edit_folder').length==0){
      if(editMenuOpened){
        $(".edit_menu").hide();
        editMenuOpened = false
      }
    }
  });

  $(".edit_menu a").click(function(){
    $(".edit_menu").hide();
    editMenuOpened = false
  });

  // Popup


  if($("#freeze").length>0) {
	  var freezeOffset = $("#freeze").offset().top;
  	var freezeHeight = $("#freeze").outerHeight()
  }
  $(".freeze_wrap").height(freezeHeight);
    if($(".alphabet").length>0){
    var liActive = 0;
    var liOffset = $(".alphabet").find("li:has(ul)").eq(liActive).offset().top;
    var endOffset = liOffset + $(".alphabet").find("li:has(ul)").eq(liActive).height()-freezeHeight-96;
    var startMargin = freezeHeight;
  }
  $(document).scroll(function(){
    var actScroll = $(document).scrollTop();

    if(actScroll>freezeOffset){
      $("#freeze").addClass("stopped");
    }
    if(actScroll<freezeOffset){
      $("#freeze").removeClass("stopped");
    }

    if($(".alphabet").length>0){
      if(actScroll>=endOffset){
        liActive ++;
        liOffset = $(".alphabet").find("li:has(ul)").eq(liActive).offset().top;
        endOffset = liOffset + $(".alphabet").find("li:has(ul)").eq(liActive).height()-freezeHeight-96;
        $(".alphabet").find("li:has(ul)").eq(liActive-1).removeClass("active").addClass("scrolled");
      }
      if(actScroll>=(liOffset-startMargin)){
        $(".alphabet").find("li:has(ul)").eq(liActive).addClass("active");
        changeActiveLetter(liActive);
      }

      if(actScroll<(liOffset-startMargin)){
        $(".alphabet").find("li:has(ul)").eq(liActive).removeClass("active");
        
        if( liActive>0){
          liActive --;
          liOffset = $(".alphabet").find("li:has(ul)").eq(liActive).offset().top;
          endOffset = liOffset + $(".alphabet").find("li:has(ul)").eq(liActive).height()-freezeHeight-96;
        }
        
      }
      if(actScroll<endOffset && actScroll>liOffset){
        changeActiveLetter(liActive);
         $(".alphabet").find("li:has(ul)").eq(liActive).addClass("active").removeClass("scrolled");
      }

    }

  });


  function changeActiveLetter(liActive){
    var attrLetter = $(".alphabet").find("li:has(ul)").eq(liActive).attr("attr-letter");
    $("#alphabet_menu").find(".active").removeClass("active");
    $("#alphabet_menu").find("a[attr-letter='"+attrLetter+"']").closest("li").addClass("active");
  }

  $(".go_top a").click(function(e){
    e.preventDefault();
    $("body, html").animate({ scrollTop:0 });
  });

  $("#alphabet_menu a").click(function(e){
    e.preventDefault();
    var attrLetter = $(this).attr("attr-letter");
    var goToLetter =  $(".alphabet").find("li[attr-letter='"+attrLetter+"']:has(ul)").offset().top-freezeHeight+1;
    // alert(goToLetter);
    $("body, html").animate({scrollTop: goToLetter})
  })

  $(".mobile_alphabet").find("select").change(function(){
    var attrLetter = $(this).find("option:selected").attr("value");
    var goToLetter = $(".alphabet").find("li[attr-letter='"+attrLetter+"']").offset().top;
    // alert(goToLetter);
    $("body, html").animate({scrollTop: goToLetter});
  })

});
