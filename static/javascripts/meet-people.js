
// Meet People carousel
(function($) {
   
   var _center = { scale: 1, left:0, marginTop: 0, left:-30, opacity: 1 	};
   var _left   = { scale: .85, marginTop: 10, left: 185, opacity: 0.3 };
   var _right  = { scale: .85, left: -235, marginTop: 10, opacity: 0.3 };	
   var _blur   = { filter : 'blur(3px)', webkitFilter: 'blur(3px)', mozFilter : 'blur(3px)', filter: 'url({{ MEDIA_URL }}/stylesheets/blur.svg#blur)' };	
   var _noblur = { filter: 'none', webkitFilter: 'none', mozFilter: 'none' }
	
	$('#meet-profiles').carouFredSel({
		auto : false,
		width: 632,
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
            console.log(data);
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
					data.items.visible.eq( 0 ).removeAttr('focused');
					data.items.visible.eq( 1 ).css({ zIndex: 3 });
					data.items.visible.eq( 1 ).attr('focused', 'true');
					data.items.visible.eq( 2 ).css({ zIndex: 2 });
					data.items.visible.eq( 2 ).removeAttr('focused');
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

	$('#ask-about').carouFredSel({
		auto : false,
		width: 213,
		height: 150,
		prev: "#ask-prev",
		next: "#ask-next",
		items: {
			visible: 1
		},
		scroll: {
			fx: 'fade',
			items: 1
		}
	});

	var setCurrentPerson = function (){
		setTimeout(function (){
			var currentlyFocusedElem = null;
	    	$('#meet-profiles li').each(function(){
	    		if($(this).attr("focused") == "true"){
	    			currentlyFocusedElem = $(this);
	    			// console.log(currentlyFocusedElem);
	    		}
	    	});
	    	Mutuality.mpcache.current = currentlyFocusedElem.attr("facebookID");
	    	console.log(currentlyFocusedElem.attr("facebookID"));
	    }, 10);
	    
	}

	$('#page-next').click(function(){
		setCurrentPerson();
		setTimeout(function (){
			var profile = Mutuality.getFriendOfFriendProfile(Mutuality.mpcache.current);

			if(profile.location){
				$("#profile-location").html(profile.location);
			}

			$(".profile-name").html(profile.name);
			$("#view-fb a").attr('onclick', Mutuality.getFacebookPageURL(profile.facebookID));
		}, 10);
	});
		$('#page-prev').click(function(){
		setCurrentPerson();
		setTimeout(function (){
			var profile = Mutuality.getFriendOfFriendProfile(Mutuality.mpcache.current);

			if(profile.location){
				$("#profile-location").html(profile.location);
			}

			$("#profile-name").html(profile.name);
			$("#view-fb a").attr('onclick', Mutuality.getFacebookPageURL(profile.facebookID));
		}, 10);
	});
    // After AJAX call for finding friends of friends, load that into meet people page cache
    var friendsOfFriendsSuccess = function(friends){
    	Mutuality.mpcache.fofList = friends;
    	meetProfilesElem = $("#meet-profiles")
    	loadingProfilesElems = $(".meet-profile");

    	for (i=0; i<friends.length; i++){
    		var liElem = $('<li>', {class:'meet-profile', facebookID:friends[i].facebookID}).appendTo(meetProfilesElem);
    		var aElem = $('<a>', {href:'#', class:"loaded"}).appendTo(liElem);
    		var imgElem = $('<img>', {src:Mutuality.getProfilePictureURL(friends[i].facebookID, 350, 350)}).appendTo(aElem);
    		var spanElem = $('<span>', {class:"match-profile-details"}).appendTo(aElem);
    		var spanElem2 = $('<span>', {id:"add-to-fav", html:"Add to Favorites"}).appendTo(spanElem);
    		var hElem = $('<h3>', {id:"left-profile-name", html:friends[i].name}).appendTo(spanElem);
    	}
    	// remove the loaders and simulate a click
    	loadingProfilesElems.each(function(){$(this).remove();});
    	$('#page-next').trigger('click');

    	
    }

   // Load friendslist and friends of friends via AJAX and populate the left and right
   // slots with a random match.
   Mutuality.loadFriendsList(null, function(){});
   Mutuality.getFriendsOfFriends(friendsOfFriendsSuccess);


})(jQuery);