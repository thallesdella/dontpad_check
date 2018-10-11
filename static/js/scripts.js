$(function(){
  ul = $('#j_mod')
  if(ul.length > 0){
    setInterval(function(){
      $.getJSON(ul.attr('data-page'), function(data){
          if(data.ul){
            ul.html(data.ul)
          }else{
            ul.html(data.msg)
          }
      });
    }, 3000);
  }
});
