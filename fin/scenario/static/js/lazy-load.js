jQuery(document).ready(function() {
    'use strict';
    var win = $(window);
    var doc = $(document);
    var loading = $('#loading');
    var active = $( "#posts" ).is( ".active" );

    // Each time the user scrolls
    win.on('scroll', function() {

    /* If scroll is end of page loading new posts */
    if ( doc.height() - win.height() - 80 < win.scrollTop() && active ) {

    loading.show();

    //Realtime likes and follows


        <script>
     $(document).ready(function(){
          function updateText(btn, newCount, verb){
          btn.text(newCount + " " + verb)
      }

      $("#follow").unbind("click").click(function(e){
        e.preventDefault()
        event.stopPropagation()
        var this_ = $(this)
        var FollowUrl = this_.attr("data-href")
        if (FollowUrl){
           $.ajax({
            url: FollowUrl,
            method: "GET",
            data: {},
            success: function(data){
              console.log(data)
              if (data.following){
                  updateText(this_, "", "Unfollow")
                  $('#follower-count').html(data.num_followers);


              } else {
                  updateText(this_, "", "Follow")
                  $('#follower-count').html(data.num_followers - 1);

                  // remove one like
              }
            }, error: function(error){
              console.log(error)
              console.log("error")
            }
          })
        }

      })
  })
    </script>


