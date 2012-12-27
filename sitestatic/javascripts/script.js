var $ = jQuery.noConflict();

$(document).ready(function(){

	// Chained interactions for thumbs up
	$("#rating-down").click( function() {
		$("#rating-buttons").fadeOut(200, function() {
			$("#reasons").fadeIn(200, function() {
				$("#done-button").click( function() {
					$("#reasons").fadeOut(200, function() {
						$("#rating-success").fadeIn(200, function() {
							$("#rating-success").delay(2000).fadeOut(200, function() {
								$("#rating-buttons").fadeIn(200);
							});
						});
					});
				});
			});
		});
	});
	
	// Thumbs up modal
	$("#buttonForModal").click(function() {
		$("#myModal").reveal();
	});
	
	// Make Matches lock
	$(".match-lock").click( function() {
		var text = $(this).text() == "Unlocked" ? "Locked" : "Unlocked";

		$(this).text(text).toggleClass("locked");
		
		return false;
	});
	
	// Search input on Make Matches
	$(".search-box").keyup( function() {
		$(this).siblings(".search-results").fadeIn(200);
	});
	$(".search-box").focusout( function() {
		$(this).siblings(".search-results").fadeOut(200);
	});

	// Meet People carousel
	$(function() {
		var _center = {
			width: 370,
			height: 370,
			marginLeft: 0,
			marginTop: 0,
			marginRight: 0,
			opacity: 1
		};
		var _left = {
			width: 340,
			height: 340,
			marginLeft: 0,
			marginTop: 15,
			marginRight: -195,
			opacity: 0.3
		};
		var _right = {
			width: 340,
			height: 340,
			marginLeft: -215,
			marginTop: 15,
			marginRight: 0,
			opacity: 0.3
		};
		var _outLeft = {
			width: 85,
			height: 85,
			marginLeft: 164,
			marginTop: 15,
			marginRight: -150,
			opacity: 0.3
		};
		var _outRight = {
			width: 85,
			height: 85,
			marginLeft: -160,
			marginTop: 15,
			marginRight: 150,
			opacity: 0.3
		};
		$('#meet-profiles').carouFredSel({
			auto : false,
			width: 647,
			height: 400,
			align: false,
			prev: "#page-prev",
			next: "#page-next",
			items: {
				visible: 3,
				width: 100
			},
			scroll: {
				items: 1,
				duration: 400,
				onBefore: function( data ) {
					data.items.old.eq( 0 ).animate(_outLeft);
					data.items.visible.eq( 0 ).animate(_left);
					data.items.visible.eq( 1 ).animate(_center);
					data.items.visible.eq( 2 ).animate(_right).css({ zIndex: 1 });
					data.items.visible.eq( 2 ).next().css(_outRight).css({ zIndex: 0 });
	
					setTimeout(function() {
						data.items.old.eq( 0 ).css({ zIndex: 1 });
						data.items.visible.eq( 0 ).css({ zIndex: 2 });
						data.items.visible.eq( 1 ).css({ zIndex: 3 });
						data.items.visible.eq( 2 ).css({ zIndex: 2 });
					}, 200);
				}
			}
		});
		$('#meet-profiles').children().eq( 0 ).css(_left).css({ zIndex: 2 });
		$('#meet-profiles').children().eq( 1 ).css(_center).css({ zIndex: 3 });
		$('#meet-profiles').children().eq( 2 ).css(_right).css({ zIndex: 2 });
		$('#meet-profiles').children().eq( 3 ).css(_outRight).css({ zIndex: 1 });
	});
	
});