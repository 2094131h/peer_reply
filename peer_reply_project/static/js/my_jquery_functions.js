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
