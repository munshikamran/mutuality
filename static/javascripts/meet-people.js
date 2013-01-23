
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


	$('#page-next').click(function(){
		// Hide the profile stats and mutual friends divs while new data being fetched
		$("#profile-stats ul").hide();
		$('#ask-about').html("");
		setCurrentPerson();
	});

	$('#page-prev').click(function(){
		// Hide the profile stats and mutual friends divs while new data being fetched
		$("#profile-stats ul").hide();
		$('#ask-about').html("");
		setCurrentPerson();
	});

	$('#fav-filter').bind('change', function(e){
		if ($('#fav-filter').val() == "Favorites"){
	        Mutuality.getFavoritesList(function(favorites){
	        	loadFavorites(favorites);
	        });
    	}
    	else{
    		friendsOfFriendsSuccess(Mutuality.mpcache.fofList);
    	}
	});

	var setCurrentPerson = function (){
		setTimeout(function (){
			var currentlyFocusedElem = null;
	    	$('#meet-profiles li').each(function(){
	    		if($(this).attr("focused") == "true"){
	    			currentlyFocusedElem = $(this);
	    		}
	    	});
	    	Mutuality.mpcache.current = currentlyFocusedElem.attr("facebookID");
	    	console.log(currentlyFocusedElem.attr("facebookID"));
	    	console.log(Mutuality.mpcache.profileCacheFbId);
	    	console.log(Mutuality.mpcache.profileCacheData);


	    	if(Mutuality.mpcache.profileCacheFbId.indexOf(Mutuality.mpcache.current) > -1) {
	    		// Cache hit, so load directly from cache!
	    		console.log("cache hit!")
	    		loadMutualFriendsIntoUI(Mutuality.mpcache.current, Mutuality.mpcache.profileCacheData[Mutuality.mpcache.current].mutualFriends);
				loadProfileInfoIntoUI(Mutuality.mpcache.current, Mutuality.mpcache.profileCacheData[Mutuality.mpcache.current].extendedProfile);
	    	}
	    	else {
	    		//Cache miss
	    		//Go fetch the data, and store it in the cache, then load from cache
	    		console.log("cache miss.")
	    		$('#page-next').hide();
	    		$('#page-prev').hide();
				setTimeout(function (){
					fetchMeetPeopleProfileInfo(Mutuality.mpcache.current);
				}, 10);

	    	}
	    }, 10);
	    
	}


    var loadMeetPeopleProfileInfoToCache = function (facebookID, mutualFriends, extendedProfile){
    	Mutuality.mpcache.profileCacheFbId.push(facebookID);
    	Mutuality.mpcache.profileCacheData[facebookID] = {
    		'mutualFriends' : mutualFriends,
    		'extendedProfile' : extendedProfile
    	}
    }


	// Fetch the extended profile and mutual friends, store in cache, and display in UI
	var fetchMeetPeopleProfileInfo = function (facebookID){
		Mutuality.getMeetPeopleProfile(facebookID, function(extendedProfile){
			Mutuality.getMutualFriendList(facebookID, function(mutualFriends){
					loadMeetPeopleProfileInfoToCache(facebookID, mutualFriends, extendedProfile);
					loadMutualFriendsIntoUI(facebookID, Mutuality.mpcache.profileCacheData[facebookID].mutualFriends);
					loadProfileInfoIntoUI(facebookID, Mutuality.mpcache.profileCacheData[facebookID].extendedProfile);
					$('#page-next').show();
					$('#page-prev').show();
			});
		});
	}

	// Fetch the extended profile and mutual friends, store in cache, and DO NOT display in UI
	var fetchMeetPeopleProfileInfoNoShow = function (facebookID, friends){
		Mutuality.getMeetPeopleProfile(facebookID, function(extendedProfile){
			Mutuality.getMutualFriendList(facebookID, function(mutualFriends){
					loadMeetPeopleProfileInfoToCache(facebookID, mutualFriends, extendedProfile);
					//Show the main content and dismiss the modal
			    	$("#main").show();
			   		$(".close-reveal-modal").trigger('click');


			    	meetProfilesElem = $("#meet-profiles")
			    	loadingProfilesElems = $(".meet-profile");

			    	for (i=0; i<friends.length; i++){
				    	var setFavoriteFunctionString = "Mutuality.setFavorite(" +friends[i].facebookID+", function(success){ console.log(success); });"
			    		var liElem = $('<li>', {class:'meet-profile', facebookID:friends[i].facebookID}).appendTo(meetProfilesElem);
			    		var aElem = $('<a>', {href:'#', class:"loaded"}).appendTo(liElem);
			    		var imgElem = $('<img>', {src:Mutuality.getProfilePictureURL(friends[i].facebookID, 350, 350)}).appendTo(aElem);
			    		var spanElem = $('<span>', {class:"match-profile-details"}).appendTo(aElem);
			    		var spanElem2 = $('<span>', {id:"add-to-fav", html:"Add to Favorites", onclick:setFavoriteFunctionString}).appendTo(spanElem);
			    		var hElem = $('<h3>', {id:"left-profile-name", html:friends[i].name}).appendTo(spanElem);
			    	}

			    	// remove the loaders and simulate a click
			    	loadingProfilesElems.each(function(){$(this).remove();});
			    	$('#page-next').trigger('click');
					});
		});
	}

	// Load the mutual friends into the UI
	var loadMutualFriendsIntoUI = function (facebookID, mutualFriends){
		var newUlElem;
		for (i=0; i<mutualFriends.length; i++){
			askaboutElem = $('#ask-about');
			if (i % 6 == 0){
				newUlElem = $('<ul>', {style: "margin-right: 0px;"}).appendTo(askaboutElem);
			}

			var liElem = $('<li>', {}).appendTo(newUlElem);
    		var aElem = $('<a>', {href:'#', onclick: Mutuality.getSendNudgeURL(Mutuality.cache.facebookID, mutualFriends[i].facebookID, "Hey can you introduce me to "+ mutualFriends[i].name + " ?", "mymutuality.com", "http://mymutuality.com/makematches")
}).appendTo(liElem);
    		var spanElem = $('<span>', {class: 'profile-thumb', style:'background-image: url(' + Mutuality.getProfilePictureURL(mutualFriends[i].facebookID)+ ');'}).appendTo(aElem);
		}
	}

	// Load the profile info into the UI
	var loadProfileInfoIntoUI = function(facebookID, extendedProfile){
		var basicProfile = Mutuality.getFriendOfFriendProfile(facebookID);
			if(basicProfile.location) {
				$("#profile-location").html('<i class="location"></i>' + basicProfile.location);
				$("#profile-location").show();
			}
			else {
				$("#profile-location").hide();
			}
			if(extendedProfile.gender) {
				$("#profile-sex").html('<i class="male"></i>' + extendedProfile.gender);
				$("#profile-sex").show();
			}
			else {
				$("#profile-sex").hide();
			}
			if(extendedProfile.relationshipStatus) {
				$("#profile-status").html('<i class="single"></i>' + extendedProfile.relationshipStatus);
				$("#profile-status").show();
			}
			else {
				$("#profile-status").hide();
			}
			if(extendedProfile.age) {
				$("#profile-dob").html('<i class="birthday"></i>' + extendedProfile.age);
				$("#profile-dob").show();
			}
			else {
				$("#profile-dob").hide();
			}			
			if(extendedProfile.college) {
				$("#profile-education").html('<i class="edu"></i>' + extendedProfile.college);
				$("#profile-education").show();
			}
			else {
				$("#profile-education").hide();
			}
			if(extendedProfile.employer) {
				$("#profile-job").html('<i class="company"></i>' + extendedProfile.employer);
				$("#profile-job").show();
			}
			else {
				$("#profile-job").hide();
			}

			$("#profile-stats ul").show();
			$(".profile-name").html(basicProfile.name);
			$("#view-fb a").attr('onclick', Mutuality.getFacebookPageURL(basicProfile.facebookID));
	}

    //After AJAX call for finding friends of friends, load that into meet people page cache
    var friendsOfFriendsSuccess = function(friends){
    	Mutuality.mpcache.fofList = friends;
    	for (i=0; i<3&&i<friends.length; i++){
    		fetchMeetPeopleProfileInfoNoShow(friends[i].facebookID, friends);
    		console.log(friends[i].facebookID);
    	}
    }

    var loadFavorites = function (favorites){
    	Mutuality.mpcache.favoritesList = favorites;
    	$("#meet-profiles").html("");

    	for (i=0; i<favorites.length; i++){
	    	//var setFavoriteFunctionString = "Mutuality.setFavorite(" +friends[i].facebookID+", function(success){ console.log(success); });"
    		var liElem = $('<li>', {class:'meet-profile', facebookID:favorites[i].facebookID}).appendTo(meetProfilesElem);
    		var aElem = $('<a>', {href:'#', class:"loaded"}).appendTo(liElem);
    		var imgElem = $('<img>', {src:Mutuality.getProfilePictureURL(favorites[i].facebookID, 350, 350)}).appendTo(aElem);
    		var spanElem = $('<span>', {class:"match-profile-details"}).appendTo(aElem);
    		//var spanElem2 = $('<span>', {id:"add-to-fav", html:"Add to Favorites", onclick:setFavoriteFunctionString}).appendTo(spanElem);
    		var hElem = $('<h3>', {id:"left-profile-name", html:favorites[i].name}).appendTo(spanElem);
    	}
    	$('#page-next').trigger('click');
    }

    var setFavorite = function (fbID){
    	Mutuality.setFavorite(fbID, function(success){
    		console.log(success);
    	});

    }

    var populateCTA = function(){
    	// TODO: Finish
    	var friends = Mutuality.cache.friends;
    	console.log(Mutuality.cache.friends);
        // friends.sort(function() { return 0.5 - Math.random();}) // shuffle the array
        /*$('#four-images img').each(function(i) {
            $(this).attr('src', Mutuality.getProfilePictureURL(friends[i].facebookID, 84, 84));
        });*/
    }

   // Load friendslist and friends of friends via AJAX and populate the left and right
   // slots with a random match.
   $("#triggerModal").trigger('click')
   $("#main").hide();
   Mutuality.loadFriendsList(populateCTA());
   Mutuality.getMeetPeople(friendsOfFriendsSuccess);



})(jQuery);