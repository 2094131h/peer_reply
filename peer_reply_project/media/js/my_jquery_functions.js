$(document).ready(function (){
  
        $('.inner_link').css({
            position:'absolute',
            left: ($('.link_button').width() - $('.inner_link').outerWidth())/2,
            top: ($('.link_button').height() - $('.inner_link').outerHeight())/2
        });

    $(.inner_link).resize();
});
