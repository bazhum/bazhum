jQuery(document).ready(function($) {
  
  jQuery.fn.gridPreview = function(options) {

    var settings = $.extend({
      'columns': 12,
      'columnClass': 'grid_1',
      'line': 20,
      'modul': 2,
      'toggleGrid': 'g', 
      'toggleZindex': 'f',
      'showAtStart': true,
      'showOnTop': false,
      'gridOpacity': '0.5',
      'gridColor': '#66ffcc',
      'topOffset': 0,
      'leftOffset': 20
    }, options);

    // Set conteiner position to "relative"
    this.css({
      "position":"relative"
    })

    // Get grid height & width
    var docHeight = $(document).height();
    var windHeight = $(window).height();
    if (docHeight<windHeight){
      var gridHeight = windHeight;
    }
    else {
      var gridHeight = docHeight-this.offset().top
    };
    var gridWidth = this.outerWidth() - settings.leftOffset;

    // Append Grid Conteiner
    this.append('<div id="gridPreviewHolder"></div>');
    var gridPreviewHolder = this.find("#gridPreviewHolder");
    gridPreviewHolder.css({
      "position": "absolute",
      "top": settings.topOffset,
      "left": settings.leftOffset,
      "height": gridHeight - settings.topOffset,
      "width": gridWidth - settings.leftOffset,
      "opacity": settings.gridOpacity
    });

    // Check grid position and display setting and do stuff
    if(settings.showAtStart == false){
      gridPreviewHolder.addClass("hidden");
      gridPreviewHolder.css({
        "display": "none"
      })
    };
    if(settings.showOnTop == true){
      gridPreviewHolder.addClass("ontop");
      gridPreviewHolder.css({
        "z-index": "9999"
      })
    }
    else{
      gridPreviewHolder.css({
        "z-index": "-1"
      })
    };

    // Append Сolumns
    for (var i = 0; i < settings.columns; i++) {
      gridPreviewHolder.append('<div class="'+settings.columnClass+'"><div class="gridPreview_column"></div></div>')
      gridPreviewHolder.find("."+settings.columnClass).eq(i).css({
        "height": "100%",
      })
      gridPreviewHolder.find(".gridPreview_column").eq(i).css({
        "height": "100%",
        "border-left":"1px solid "+settings.gridColor+"",
        "border-right":"1px solid "+settings.gridColor+""
      })
    };

    // Append lines
    var linesNumber = Math.floor(gridHeight/settings.line);
    for (var i = 0; i < linesNumber; i++) {
      gridPreviewHolder.append('<div class="gridPreview_line"></div>')
      var thisLine = gridPreviewHolder.find(".gridPreview_line").eq(i);
      thisLine.css({
        "height": settings.line,
        "border-top":"1px solid "+settings.gridColor+""
      })
      for (var j = 0; j < settings.modul; j++) {
        thisLine.append("<div class='smaller_line'></div>")
        if (j!=(settings.modul-1)){
          thisLine.find('.smaller_line').eq(j).css({
            "border-bottom":"1px dotted "+settings.gridColor+"",
            "height": thisLine.outerHeight()/settings.modul
          })
        }
        else{
          thisLine.find('.smaller_line').eq(j).css({
            "height": thisLine.outerHeight()/settings.modul
          })
        }
      }
      };

      // Focus or not
      var focused = false;
      $("input, password, textarea").focusin(function(){
        focused = true;
      })
      $("input, password, textarea").focusout(function(){
        focused = false;
      });

      // Toggle functions
      var toggleGridFunction = function(){
          if(gridPreviewHolder.hasClass('hidden')){
            gridPreviewHolder.removeClass('hidden');
            gridPreviewHolder.css({
              "display":"block"
            });
          }
          else{
            gridPreviewHolder.addClass('hidden');
            gridPreviewHolder.css({
              "display":"none"
            });
          }
      }

      var toggleZindexFunction = function(){
         if(gridPreviewHolder.hasClass('ontop')){
              gridPreviewHolder.removeClass('ontop');
              gridPreviewHolder.css({
                "z-index":"-1"
              })     
            }
            else{
              gridPreviewHolder.addClass('ontop');
              gridPreviewHolder.css({
                "z-index":"9999"
              })
          }         
      };

      // Show grid
      var keyToggle = settings.toggleGrid.charCodeAt();
      var keyZindex = settings.toggleZindex.charCodeAt();
 
      $(document).keypress(function(e){
        if(focused==false){
          if ( e.keyCode == keyToggle ) {
            toggleGridFunction();
          }
          if ( e.keyCode == keyZindex ) {
            toggleZindexFunction();
          }
        }
      });


        
  };  






});
