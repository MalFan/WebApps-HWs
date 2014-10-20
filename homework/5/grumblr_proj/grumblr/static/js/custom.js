// Customized javascript via jQuery
$(document).ready( function() {


	$(".form-comment").submit(function(e)
	{
		var postData = $(this).serializeArray();
		var formURL = $(this).attr("action");
		var id = $( this ).attr( "grumbl-id" );
		$.ajax(
		{
			url : formURL,
			type: "POST",
			data : postData,
			success:function(comment) 
			{
				//data: return data from server
				alert( "success" + id );

				// new hr
				var hr = $( "<hr class=\"comment-hr\">" );
				// new comment div
				var comment_div = $( "div.post-comments" ).eq( 0 ).clone();
				var current_username = $( "li.dropdown a" ).first().contents().filter(function() {
					return this.nodeType == 3;
				}).text();
				current_username = current_username.substring(1, current_username.length - 1)
				comment_div.children( "div.post-title" ).children( "div.post-avatar" ).children().attr( "href", "/profile/" + comment[0].fields.user );
				comment_div.children( "div.post-title" ).children( "div.post-avatar" ).children().children().attr( {
					src: "/get-photo/" + current_username,
					alt: current_username
				});
				alert( current_username + comment[0].fields.pub_time + comment[0].fields.text );
				comment_div.children( "div.post-title" ).children( "div.post-user" ).children().first().html( current_username );
				comment_div.children( "div.post-title" ).children( "div.post-user" ).children().last().html( comment[0].fields.pub_time );
				comment_div.children( "div.post-content" ).children().html( comment[0].fields.text );

				$( "div.post-write-comment[grumbl-id=" + id + "]" ).after( comment_div );
				$( "div.post-write-comment[grumbl-id=" + id + "]" ).after( hr );			    
			},
			error: function() 
			{
				//if fails
				alert( "error" );      
			}
		});
		e.preventDefault(); //STOP default action
	});




	// $( ".comment-btn" ).click(function( event ) {

	// 	var id = $( this ).attr( "grumbl-id" );
	// 	var form_data = $( this ).parents( ".form-comment" ).serialize();

	// 	// $.ajaxSetup({ 
	// 	//      beforeSend: function(xhr, settings) {
	// 	//          function getCookie(name) {
	// 	//              var cookieValue = null;
	// 	//              if (document.cookie && document.cookie != '') {
	// 	//                  var cookies = document.cookie.split(';');
	// 	//                  for (var i = 0; i < cookies.length; i++) {
	// 	//                      var cookie = jQuery.trim(cookies[i]);
	// 	//                      // Does this cookie string begin with the name we want?
	// 	//                  if (cookie.substring(0, name.length + 1) == (name + '=')) {
	// 	//                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	// 	//                      break;
	// 	//                  }
	// 	//              }
	// 	//          }
	// 	//          return cookieValue;
	// 	//          }
	// 	//          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
	// 	//              // Only send the token to relative URLs i.e. locally.
	// 	//              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	// 	//          }
	// 	//      } 
	// 	// });

	// 	// $.ajax(
	// 	// {
	// 	// 	url : "/add-comment/" + id,
	// 	// 	type: "POST",
	// 	// 	data : form_data,
	// 	// 	success:function(response) 
	// 	// 	{
	// 	// 		//data: return data from server
	// 	// 		alert( "success" );
	// 	// 		alert( response );
	// 	// 		// var comment = $.parseJSON(response);
				
	//  //  			// new hr
	// 	// 		var hr = $( "<hr class=\"comment-hr\">" );
	// 	// 		// new comment div
	// 	// 		var comment_div = $( ".post-comments:first" ).clone();
	// 	// 		comment_div.children( "div.post-avatar" ).children().attr( "href", "{% url 'profile' comment.user.id %}" );
	// 	// 		comment_div.children( "div.post-avatar" ).children().children().attr( {
	// 	// 			src: "{% url 'getphoto' comment.user.username %}",
	// 	// 			alt: "{{comment.user.username}}"
	// 	// 		} );
	// 	// 		// comment_div.children( "div.post-user" ).children().first().html( {{comment.user.username}} );
	// 	// 		// comment_div.children( "div.post-user" ).children().last().html( {{comment.pub_time}} );
	// 	// 		// comment_div.children( "div.post-content" ).children().html( {{comment.text}} );

	// 	// 		$( "div.post-write-comment" ).after( comment_div );
	// 	// 		$( "div.post-write-comment" ).after( hr );
	// 	// 	},
	// 	// 	error: function() 
	// 	// 	{
	// 	// 	    //if fails 
	// 	// 	    alert( "error" );     
	// 	// 	}
	// 	// });
	// });
});






