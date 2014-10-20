// Customized javascript via jQuery
$(document).ready( function() {

	$(".form-comment").submit(function(e)
	{
		var post_data = $(this).serializeArray();
		var form_url = $(this).attr("action");
		var id = $( this ).attr( "grumbl-id" );
		$.ajax(
		{
			url : form_url,
			type: "POST",
			data : post_data,
			success:function(comment) 
			{
				// alert( "success" + id );

				// new hr
				var hr = $( "<hr class=\"comment-hr\">" );
				
				var current_username = $( "li.dropdown a" ).first().contents().filter(function() {
					return this.nodeType == 3;
				}).text();
				current_username = current_username.substring(1, current_username.length - 1)			

				// new comment div
              		var div_post_comments = $( "<div class=\"post-comments\"></div>" );
              		var div_post_title = $( "<div class=\"post-title\"></div>" );
				var div_post_content = $( "<div class=\"post-content\"></div>" );
				div_post_comments.append( div_post_title );
				div_post_comments.append( div_post_content );

				var div_post_avatar = $( "<div class=\"post-avatar\"></div>" );
				var div_post_user = $( "<div class=\"post-user\"></div>" );
				div_post_title.append( div_post_avatar );
				div_post_title.append( div_post_user );

				var img_href = $( "<a/>", { href: "/profile/" + comment[0].fields.user } );
				div_post_avatar.append( img_href );
				img_href.append( $( "<img>", { 
					src: "/get-photo/" + current_username,
					alt: current_username,
					width: "64px"
				} ) );
				div_post_user.append( "<p class=\"grumblr-name\">" + current_username + "</p>" );
				div_post_user.append( "<p>" + comment[0].fields.pub_time + "</p>" );
				div_post_content.append( "<p>" + comment[0].fields.text + "</p>" )

				// Append new comment.
				$( "div.post-write-comment[grumbl-id=" + id + "]" ).after( div_post_comments );
				$( "div.post-write-comment[grumbl-id=" + id + "]" ).after( hr );

				// Change the reply count.
				$( "form[grumbl-id=" + id + "] input[name='grumbl_comment']" ).val( "" );
				var current_text = $( "a.reply-btn[grumbl-id=" + id + "]" ).children().last().html();
				current_replys = current_text.substring(current_text.indexOf("(") + 1, current_text.indexOf(")"))
				var new_replys = parseInt(current_replys, 10) + 1;
				new_text = current_text.replace(current_replys, new_replys);
				$( "a.reply-btn[grumbl-id=" + id + "]" ).children().last().html( new_text );			    
			},
			error: function() 
			{
				//if fails
				alert( "error" );      
			}
		});
		e.preventDefault(); //STOP default action
	});


	$( "a.dislike-btn" ).click(function( e ) {		

		var id = $( this ).attr( "grumbl-id" );
		var btn_href = "/dislike/" + id
		$.ajax(
		{
			url : btn_href,
			success:function(response) 
			{
				// alert( "success" );

				var current_text = $( "a.dislike-btn[grumbl-id=" + id + "]" ).children().last().html();
				current_dislikes = current_text.substring(current_text.indexOf("(") + 1, current_text.indexOf(")"))
				
				// alert( current_dislikes );
				var new_dislikes = parseInt(current_dislikes, 10) + parseInt(response, 10);
				// alert( new_dislikes );
				new_text = current_text.replace(current_dislikes, new_dislikes);
				$( "a.dislike-btn[grumbl-id=" + id + "]" ).children().last().html( new_text );
					
			},
			error: function() 
			{
			    //if fails 
			    alert( "error" );     
			}
		});
		e.preventDefault(); //STOP default action
	});


});






