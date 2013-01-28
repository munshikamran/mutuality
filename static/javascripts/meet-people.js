
(function($) {
   /* Begin Meet People Carousel Code */
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
            console.log(data.items.visible);

            for(i=0; i<data.items.visible.length; i++){
            	var facebookID = $(data.items.visible[i]).attr("facebookid");
            	if(Mutuality.mpcache.profileCacheFbId.indexOf(facebookID) === -1){
					Mutuality.getMeetPeopleProfile(facebookID, function(extendedProfile){
						Mutuality.getMutualFriendList(facebookID, function(mutualFriends){
							loadMeetPeopleProfileInfoToCache(facebookID, mutualFriends, extendedProfile);
						});
					});
				}
            }

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

/* End Meet People Carousel Code */
/* Begin Event Code */

	// Drop down the modal when you click "Get introduced"
	$('#introduce').click(function(){
		var basicProfile = Mutuality.getFriendOfFriendProfile(Mutuality.mpcache.current);
		$('#myModal2Header').html("Why don't you ask a friend to connect you and " + basicProfile.name + "?");
	});

	// When you click next, set the current person
	$('#page-next').click(function(){
		// Hide the profile stats and mutual friends divs while new data being fetched
		$("#profile-stats ul li").hide();
		$('#ask-about').html("");
		setCurrentPerson();
	});

	// When you click previous, set the current person as well
	$('#page-prev').click(function(){
		// Hide the profile stats and mutual friends divs while new data being fetched
		$("#profile-stats ul li").hide();
		$('#ask-about').html("");
		setCurrentPerson();
	});

	// When the fav filter is selected, load the favorites into the UI
	$('#fav-filter').bind('change', function(e){
		if ($('#fav-filter').val() == "Favorites"){
        	loadFavorites(Mutuality.mpcache.favoritesList);
    	}
    	else{
    		friendsOfFriendsSuccess(Mutuality.mpcache.fofList);
    	}
	});
/* End Event Code */
/* Begin Helper functions */

	// Find out which person is currently focused and get their details
	var setCurrentPerson = function (){
		setTimeout(function (){
			var currentlyFocusedElem = null;
	    	$('#meet-profiles li').each(function(){
	    		if($(this).attr("focused") == "true"){
	    			currentlyFocusedElem = $(this);
	    		}
	    	});

	    	Mutuality.mpcache.current = currentlyFocusedElem.attr("facebookID");
	    	//console.log(currentlyFocusedElem.attr("facebookID"));
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
	    		//Go fetch the data, and store it in the cache, then load into UI from cache
	    		console.log("cache miss.")
	    		$('#page-next').hide();
	    		$('#page-prev').hide();
				setTimeout(function (){
					fetchMeetPeopleProfileInfo(Mutuality.mpcache.current);
				}, 50);

	    	}
	    }, 50);
	    
	}

	// Store meet people profile and mutual friends into cache object
    var loadMeetPeopleProfileInfoToCache = function (facebookID, mutualFriends, extendedProfile){
    	Mutuality.mpcache.profileCacheFbId.push(facebookID);
    	Mutuality.mpcache.profileCacheData[facebookID] = {
    		'mutualFriends' : mutualFriends,
    		'extendedProfile' : extendedProfile
    	}
    }

	// Fetch the extended profile and mutual friends, store in cache, and then display in UI
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

	// Fetch the list of friends returned from getMeetPeople, put into carousel, store in cache
	var fetchMeetPeopleProfileInfoAndShowUI = function (facebookID, friends){
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
			    		var inFavorites = false;
			    		/*for (i=0;i<Mutuality.mpcache.favoritesList; i++){
			    			if (Mutuality.mpcache.favoritesList[i].facebookID === friends[i].facebookID){
			    				inFavorites= true;
			    			}
			    		}*/
			    		if (!inFavorites) {
			    			var spanElem2 = $('<span>', {id:"add-to-fav", html:"Add to Favorites", onclick:setFavoriteFunctionString}).appendTo(spanElem);
			    		}
			    		else{
			    			var spanElem2 = $('<span>', {id:"add-to-fav", html:"Add to Favorites", style:"background-position: 0 -16px;"}).appendTo(spanElem);
			    			console.log("yes a favorite");
			    		}
			    		var hElem = $('<h3>', {id:"left-profile-name", html:friends[i].name}).appendTo(spanElem);
			    	}

			    	// remove the loaders and simulate a click
			    	loadingProfilesElems.each(function(){$(this).remove();});
			    	$('#page-next').trigger('click');
				});
		});
	}

	// Just load the current person's mutual friends into the UI
	var loadMutualFriendsIntoUI = function (facebookID, mutualFriends){
		var newUlElem;
		for (i=0; i<mutualFriends.length; i++){
			askaboutElem = $('#ask-about');
			askaboutElemModal = $('#ask-about-modal');
			if (i % 6 == 0){
				newUlElem = $('<ul>', {style: "margin-right: 0px;"}).appendTo(askaboutElem);
				newUlElemModal = $('<ul>', {style: "margin-right: 0px;"}).appendTo(askaboutElemModal);
			}

			var liElem = $('<li>', {}).appendTo(newUlElem);
			var liElemModal = $('<li>', {}).appendTo(newUlElemModal);
    		var aElem = $('<a>', {onclick: Mutuality.getSendNudgeURL(Mutuality.cache.facebookID, mutualFriends[i].facebookID, "Hey can you introduce me to "+ mutualFriends[i].name + " ?", "mymutuality.com", "http://mymutuality.com/makematches")
}).appendTo(liElem);
    		var aElemModal = $('<a>', {onclick: Mutuality.getSendNudgeURL(Mutuality.cache.facebookID, mutualFriends[i].facebookID, "Hey can you introduce me to "+ mutualFriends[i].name + " ?", "mymutuality.com", "http://mymutuality.com/makematches")
}).appendTo(liElemModal);
    		var spanElem = $('<span>', {class: 'profile-thumb', style:'background-image: url(' + Mutuality.getProfilePictureURL(mutualFriends[i].facebookID)+ ');'}).appendTo(aElem);
    		var spanElemModal = $('<span>', {class: 'profile-thumb', style:'background-image: url(' + Mutuality.getProfilePictureURL(mutualFriends[i].facebookID)+ ');'}).appendTo(aElemModal);
		}
	}

	// Load the current person's profile info into the UI
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

    // After AJAX call for getMeetPeople, load that into meet people page cache
    var friendsOfFriendsSuccess = function(friends){
    	Mutuality.mpcache.fofList = friends;
    	for (i=2; i<3&&i<friends.length; i++){
    		fetchMeetPeopleProfileInfoAndShowUI(friends[i].facebookID, friends);
    	}
    }

    // Load the favorites into the UI
    var loadFavorites = function (favorites){
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

    // Set a favorite
    // TODO: Keep the star highlighted
    var setFavorite = function (fbID){
    	Mutuality.setFavorite(fbID, function(success){
    		console.log(success);
    	});
    }

    // Populate the CTA with actual friend data
    // TODO: Actually put in the images
    var populateCTA = function(){
    	// TODO: Finish
    	var friends = Mutuality.cache.friends;
    	console.log(Mutuality.cache.friends);
        // friends.sort(function() { return 0.5 - Math.random();}) // shuffle the array
        /*$('#four-images img').each(function(i) {
            $(this).attr('src', Mutuality.getProfilePictureURL(friends[i].facebookID, 84, 84));
        });*/
    }
 /* End Helper Functions */

/* Begin Main Code */
   // Load friendslist, get the meet people result, and make sure the loading modal displays
   $("#triggerModal").trigger('click');
   $("#main").hide();
   Mutuality.loadFriendsList(populateCTA());
   Mutuality.getMeetPeople(friendsOfFriendsSuccess);
   Mutuality.getFavoritesList(function(favorites){
    	Mutuality.mpcache.favoritesList = favorites;
   });
/* End Main Code */

})(jQuery);