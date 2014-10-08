// Insert code here to run when the DOM is ready
$(document).ready( function() {
	$( ".delete-btn" ).click(function( event ) {
 		
		var id = $( this ).attr( "data-item-id" );
		$.get( "/shared-todo-list/delete-item/" + id );
		$( this ).parent().remove();

	});
});
