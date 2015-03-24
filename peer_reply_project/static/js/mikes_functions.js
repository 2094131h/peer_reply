$(document).ready( function() {

    $(".flag").click( function(event) {
        ansid = $(this).attr("data-ansid");      
        $.get('/peer_reply/flag_answer/', {answer_id: ansid}, function(){
        alert("flagged")
        });     
    });

    $(".rate").click( function(event) {
        ansid = $(this).attr("data-ansid");      
        $.get('/peer_reply/rate_answer/', {answer_id: ansid}, function(){
        alert("rated")
        });       
    });

    $(".best").click( function(event) {
        ansid = $(this).attr("data-ansid");      
        $.get('/peer_reply/mark_as_best_answer/', {answer_id: ansid}, function(){
        alert("marked as best")
        });       
    });

    $("#rate-quiz").click( function(event) {
        quizid = $(this).attr("data-quizid");      
        $.get('/peer_reply/like_quiz/', {quiz_id: quizid}, function(){
        alert("rated")
        });       
    });


});



/**
$(document).ready( function() {

    $(".test").click(function() {
    $('#dialog-confirm').dialog('open');
    )};

// jquery-ui confirm dialog box
$("#dialog-confirm").dialog({
   autoOpen: false,
   resizable: false,
   modal: true,
   buttons: {
        'Yes': function() { // remove what you want to remove
               // do something here
         },
         Cancel: function() {
               $(this).dialog('close');
         }
   }
});
});
**/





