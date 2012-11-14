
// Meet People carousel
(function($) {
   
	var _center = {
	   scale: 1,
		left:0,
		marginTop: 0,
		opacity: 1
	};
	var _left = {
	   scale: .85,
		marginTop: 10,
		left: 215,
		opacity: 0.3
	};
	var _right = {
	   scale: .85,
		left: -215,
		marginTop: 10,
		opacity: 0.3
	};
	
	var _blur = {
      filter : 'blur(3px)',
      webkitFilter: 'blur(3px)',
      mozFilter : 'blur(3px)',
      filter: 'url(/stylesheets/blur.svg#blur)'
	};
	
	var _noblur = {
	  filter: 'none',
	  webkitFilter: 'none',
	  mozFilter: 'none'
	}
	
	$('#meet-profiles').carouFredSel({
		auto : false,
		width: 647,
		height: 400,
		align: 'center',
		prev: "#page-prev",
		next: "#page-next",
		items: {
			visible: 3,
			width: 350
		},
		scroll: {
			items: 1,
			duration: 400,
			onBefore: function( data ) {
            
            // hide the text for blurred results
            $('.match-profile-details', data.items.visible.eq( 0 )).hide();
            $('.match-profile-details', data.items.visible.eq( 2 )).hide();            

            // move visible items into position
				data.items.visible.eq( 0 ).animate(_left, function(){
				   $('img', data.items.visible.eq( 0 )).css(_blur);
				});
				data.items.visible.eq( 1 ).animate(_center, 300);
				data.items.visible.eq( 2 ).animate(_right, function(){
				   $('img', data.items.visible.eq( 2 )).css(_blur);
				});

            // reset z-indexes for smooth scrolling
				setTimeout(function() {
					data.items.visible.eq( 0 ).css({ zIndex: 2 });
					data.items.visible.eq( 1 ).css({ zIndex: 3 });
					data.items.visible.eq( 2 ).css({ zIndex: 2 });
				}, 10);
			},
			onAfter:function( data ) {
			   $('img', data.items.visible.eq( 1 )).css(_noblur);		
			   $('.match-profile-details', data.items.visible.eq( 1 )).fadeIn();	   
		   }
		}
	});
	
	// re-adjust width - think it is a border-box issue
	var wid = $('#meet-profiles').outerWidth() + ($('#meet-profiles li').length * 30);
	$('#meet-profiles').css({visibility:'visible',width: wid});
	$('#meet-profiles li').css({position:'relative'});
	
   $('.match-profile-details', $('#meet-profiles').children().eq( 0 )).hide();
   $('.match-profile-details', $('#meet-profiles').children().eq( 2 )).hide();	
	
   $('img', $('#meet-profiles').children().eq( 0 )).css(_blur);
   $('img', $('#meet-profiles').children().eq( 2 )).css(_blur);
   
	$('#meet-profiles').children().scale(.85);
	$('#meet-profiles').children().eq( 0 ).css(_left).scale(0.85).css({ zIndex: 2 });
	$('#meet-profiles').children().eq( 1 ).css(_center).scale(1.0).css({ zIndex: 3 });
	$('#meet-profiles').children().eq( 2 ).css(_right).scale(0.85).css({ zIndex: 2 });
	
})(jQuery);