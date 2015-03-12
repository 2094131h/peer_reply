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
      
