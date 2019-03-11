document.getElementById("id_content").onkeyup = function () {
      document.getElementById("char_count").innerHTML = 250 - this.value.length;
};



/*$('#like').click(function(){
      $.ajax({
               type: "POST",
               url: $(this).attr('url'),
               data: {'username': $(this).attr('username'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
               dataType: "json",
               success: function(response) {
                      alert(response.message);
                      alert('Company likes count is now ' + response.likes_count);
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });
    })*/
