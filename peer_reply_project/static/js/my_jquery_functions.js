<<<<<<< HEAD
//$(document).ready(function (){
//
//        $('.inner_link').css({
//            position:'absolute',
//            left: ($('.link_button').width() - $('.inner_link').outerWidth())/2,
//            top: ($('.link_button').height() - $('.inner_link').outerHeight())/2
//        });
//
//    $(.inner_link).resize();
//});

$(document).ready(function()  {  
    $("#search").keyup(function() {
         var search  =  $("#search").val();
         if (search.length >  0) {    
             $.ajax({type:"POST", url: "suggest/", data: "search=" + search, success:function(message{    
             $("#suggest").empty();    
             if  (message.length >  0)  {    
                  message  = "Do  you  mean: " +  message + "?";    
                  $("#suggest").append(message);    
                 }    
              }    
      });  
      }  else  {    
      //  Empty  suggestion  list    
      $("#suggest").empty();    
      }   
});  
      
=======
  <script type="text/javascript" charset="utf-­‐8">
$('label.tree-toggler').parent().children('ul.tree').toggle(0);
$(document).ready(function () {

	$('label.tree-toggler').click(function () {
        $(this).parent().find('.school_down_icon').toggleClass('glyphicon glyphicon-chevron-left glyphicon glyphicon-chevron-down');
		$(this).parent().children('ul.tree').toggle(600);
        $(this).parent().siblings().toggle(800)

	});

    $('label.tree-toggler-level').parent().children('ul.tree').toggle(600);
	$('label.tree-toggler-level').click(function () {
        $(this).parent().find('.school_down_icon').toggleClass('glyphicon glyphicon-chevron-down glyphicon glyphicon-chevron-up');
		$(this).parent().children('ul.tree').toggle(600);


	});

$('#school_select').change(function(){
        var query;
        query = $(this).val();
        $.get('/peer_reply/get_levels/', {school_id: query}, function(data){
         $('#level_select').html(data);
          $('select option:first-child').delay(5000).attr("selected", "selected");
         $( "#level_select" ).trigger( "change" );
          $("#level_select").selectpicker('refresh');
        });



});

$('#level_select').change(function(){
        var query;
        query = $(this).val();
        $.get('/peer_reply/get_courses/', {level_id: query}, function(data){
         $('#course_select').html(data);
        });
});
});

  </script>  
>>>>>>> f0998634b8c45602b46d41fdd4bdeb319fb08aaf
