
(function($) {
   /* Begin Meet People Carousel Code */
   var _center = { scale: 1, left:0, marginTop: 0, left: -20, opacity: 1 	};
   var _left   = { scale: .85, marginTop: 10, left: 152, opacity: 0.3 };
   var _right  = { scale: .85, left: -206, marginTop: 10, opacity: 0.3 };
   var _blur   = { filter : 'blur(3px)', webkitFilter: 'blur(3px)', mozFilter : 'blur(3px)', filter: 'url({{ MEDIA_URL }}/stylesheets/blur.svg#blur)' };	
   var _noblur = { filter: 'none', webkitFilter: 'none', mozFilter: 'none' }

   var MAX_CAROUSEL_NUM = 100;

	var initCarousel = function () {
		$('#meet-profiles').carouFredSel({
			auto : false,
			width: 695,
			height: 400,
			circular: true,
			align: 'center',
			prev: { button: "#page-prev" },
			next: { button: "#page-next" },
			items: {
				visible: 3,
				width: 350
			},
			scroll: {
				items: 1,
				duration: 400,
				onBefore: function( data ) {
					
					if (data.items.visible.prevObject.length > 3) {
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
					}
				},
				onAfter:function( data ) {
				   $('img', data.items.visible.eq( 1 )).css(_noblur);		
				   $('.match-profile-details', data.items.visible.eq( 1 )).fadeIn();
   					// Everytime we scroll the carousel- load data into cache	
			        for(i=0; i<5&&i<data.items.visible.prevObject.length; i++){
			        	var fbID = $(data.items.visible.prevObject[i]).attr("facebookid");
			        	if(!Mutuality.mpcache.profileCacheData[fbID]){
							fbID = $(data.items.visible.prevObject[i]).attr("facebookid");
							//console.log("Calls made for " + fbID);
							asyncCacheCalls(fbID);
						}
			        }	   
			   }
			}
		});
	}

	var asyncCacheCalls = function(fbID){
		Mutuality.getMeetPeopleProfile(fbID, function(extendedProfile){
			Mutuality.getMutualFriendList(fbID, function(mutualFriends){
	        	//console.log("Calls returned for " + fbID);
				loadMeetPeopleProfileInfoToCache(fbID, mutualFriends, extendedProfile);
			});
		});
	}

	var initAskAboutCarousel = function () {
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

		$('#ask-about-modal').carouFredSel({
		auto : false,
		width: 400,
		height: 150,
		prev: "#ask-prev-modal",
		next: "#ask-next-modal",
		items: {
			visible: 1
		},
		scroll: {
			fx: 'fade',
			items: 1
		}
	});

	};

	// Make sure that when you are scrolling with the keyboard, it's like you're clicking next/prev
	$("body").keydown(function (e){ 
	    if(e.keyCode == 37 || e.which == 37) // left arrow
	    {
	    	if($('#page-prev').is(":visible")){
	        	$('#page-prev').click();
	    	}
	    }
	    else if(e.keyCode == 39 || e.which == 39)    // right arrow
	    { 
	        if($('#page-next').is(":visible")){
	        	$('#page-next').click();
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
/* End Meet People Carousel Code */
/* Begin Event Code */

	$("#introduce").click(function(){
	    	$('#page-next').hide();
	    	$('#page-prev').hide();

	});

	// When you click next, set the current person
	$('#page-next').click(function(){
		// Hide the profile stats and mutual friends divs while new data being fetched
		$('#ask-about').html("");
		$('#ask-about-modal').html("");
		setCurrentPerson();
	});

	// When you click previous, set the current person as well
	$('#page-prev').click(function(){
		// Hide the profile stats and mutual friends divs while new data being fetched
		$('#ask-about').html("");
		$('#ask-about-modal').html("");
		setCurrentPerson();
	});

	// When the fav filter is selected, load the favorites into the UI
	$('#fav-filter').bind('change', function(e){
		if ($('#fav-filter').val() == "Favorites"){
			triggerModal();
			Mutuality.getFavoritesList(function(favorites){
        		loadNewDataIntoCarousel(favorites);
        		for (i=0;i<favorites.length; i++){
        			if (!Mutuality.mpcache.favoritesList[favorites[i].facebookID]) {
        				Mutuality.mpcache.favoritesList[favorites[i].facebookID] = true;
        			}
				}
   			});
    	} else if ($('#fav-filter').val() == "Viewed") {
		   triggerModal()
    		Mutuality.getMeetPeople(1, 0, function(viewedUsers){
    			loadNewDataIntoCarousel(viewedUsers);
    		});
    	}
    	else if ($('#fav-filter').val() == "Dating") {
    		triggerModal();
    		Mutuality.getMeetPeople(0, 1, function(datingFriends){
    			loadNewDataIntoCarousel(datingFriends);
    		});
    	}
    	else{
    		triggerModal();
    		Mutuality.getMeetPeople(0, 0, function(meetPeopleList) {
    			loadNewDataIntoCarousel(meetPeopleList);
    		});
    	}
	});

/* End Event Code */
/* Begin Helper functions */

	var triggerModal = function(){
	   $("#triggerModal").trigger('click');
	   $("page-next").hide();
	   $("page-prev").hide();
	}

	var hideModal = function(){
	   $(".close-reveal-modal").trigger('click');
	   $("page-next").show();
	   $("page-prev").show();
	}

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
	    	console.log("Current Person: "+currentlyFocusedElem.attr("facebookID"));


    		//console.log(Mutuality.mpcache.profileCacheData);	    	
    		//Mutuality.setUserViewed(Mutuality.mpcache.current, function(success){console.log("set viewed = " + success );});

	    	if(Mutuality.mpcache.profileCacheData[Mutuality.mpcache.current]) {
	    		// Cache hit, so load directly from cache!
	    		// console.log("cache hit!")
	    		loadMutualFriendsIntoUI(Mutuality.mpcache.current, Mutuality.mpcache.profileCacheData[Mutuality.mpcache.current].mutualFriends);
				loadProfileInfoIntoUI(Mutuality.mpcache.current, Mutuality.mpcache.profileCacheData[Mutuality.mpcache.current].extendedProfile);
	    	}
	    	else {
	    		//Cache miss
	    		//Go fetch the data, and store it in the cache, then load into UI from cache
	    		//console.log("cache miss.")
	    		$('#page-next').hide();
	    		$('#page-prev').hide();
				setTimeout(function (){
					fetchMeetPeopleProfileInfo(Mutuality.mpcache.current);
				}, 130);

	    	}
	    }, 130);
	    
	}

	// Store meet people profile and mutual friends into cache object
    var loadMeetPeopleProfileInfoToCache = function (facebookID, mutualFriends, extendedProfile){
    	Mutuality.mpcache.profileCacheData[facebookID] = {
    		'mutualFriends' : mutualFriends,
    		'extendedProfile' : extendedProfile
    	}
    	//console.log("Added " + facebookID);
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
					meetProfilesElem = $("#meet-profiles");
					console.log("Length of Friends = " + friends.length);
			    	for (i=0; i<MAX_CAROUSEL_NUM&&i<friends.length; i++){
	    				var setFavoriteFunctionString = "Mutuality.setFavorite(" +friends[i].facebookID+", function(success){ $('#add-to-fav').each(function(){ console.log($(this)); if($(this).attr('facebookID') =='"+friends[i].facebookID+"'){$(this).css('background-position',  '0 -16px;'); }});});"    		

			    		var liElem = $('<li>', {class:'meet-profile', facebookID:friends[i].facebookID}).appendTo(meetProfilesElem);
			    		var aElem = $('<a>', {href:'#', class:"loaded"}).appendTo(liElem);
			    		var imgElem = $('<img>', {src:Mutuality.getProfilePictureURL(friends[i].facebookID, 350, 350)}).appendTo(aElem);
			    		var spanElem = $('<span>', {class:"match-profile-details"}).appendTo(aElem);
			    		var inFavorites = Mutuality.mpcache.favoritesList[friends[i].facebookID];

			    		if (!inFavorites) {
			    			var spanElem2 = $('<span>', {id:"add-to-fav", class:"tooltip", title: "Add to Favorites", facebookID: friends[i].facebookID ,  onclick:setFavoriteFunctionString}).appendTo(spanElem);
			    		}
			    		else{
			    			var spanElem2 = $('<span>', {id:"add-to-fav", html:"Remove from Favorites", class:"tooltip", style:"background-position: 0 -16px;"}).appendTo(spanElem);
			    			//console.log("yes a favorite");
			    		}
			    		var hElem = $('<h3>', {id:"left-profile-name", html:friends[i].name}).appendTo(spanElem);
			    	}

					//Show the main content, dismiss the modal, init tooltips
			    	$("#main").show();
			    	hideModal();
		    		$('.tooltip').tooltipster();
			    	initCarousel();

			    	$('#page-next').trigger('click');

				});
		});
	}

	// Just load the current person's mutual friends into the UI
	var loadMutualFriendsIntoUI = function (facebookID, mutualFriends){
		var newUlElem;
		var currentPersonName = Mutuality.getFriendOfFriendProfile(Mutuality.mpcache.current);
		var messageString = "Hey can you introduce me to " + currentPersonName.name + "?";

		for (i=0; i<mutualFriends.length; i++){
			askaboutElem = $('#ask-about');
			askaboutElemModal = $('#ask-about-modal');
			if (i % 6 == 0){
				newUlElem = $('<ul>', {style: "margin-right: 0px;"}).appendTo(askaboutElem);
				newUlElemModal = $('<ul>', {style: "margin-right: 0px; list-style-type: none;"}).appendTo(askaboutElemModal);
			}

			var liElem = $('<li>', {}).appendTo(newUlElem);
			var liElemModal = $('<li>', {}).appendTo(newUlElemModal);
    		var aElem = $('<a>', {onclick: Mutuality.getSendNudgeURL(Mutuality.cache.facebookID, mutualFriends[i].facebookID, messageString, "http://goo.gl/L7Uk9")
}).appendTo(liElem);
    		var aElemModal = $('<a>', {onclick: Mutuality.getSendNudgeURL(Mutuality.cache.facebookID, mutualFriends[i].facebookID, messageString, "http://goo.gl/L7Uk9")
}).appendTo(liElemModal);
    		var spanElem = $('<span>', {class: 'profile-thumb tooltip', title: "Ask " + mutualFriends[i].name.split(" ")[0], style:'background-image: url(' + Mutuality.getProfilePictureURL(mutualFriends[i].facebookID)+ ');'}).appendTo(aElem);
    		var spanElemModal = $('<span>', {class: 'profile-thumb tooltip', title: "Ask " + mutualFriends[i].name.split(" ")[0], style:'background-image: url(' + Mutuality.getProfilePictureURL(mutualFriends[i].facebookID)+ ');'}).appendTo(aElemModal);
		}

		$('.tooltip').tooltipster();
		initAskAboutCarousel();
	}

	// Load the current person's profile info into the UI
	var loadProfileInfoIntoUI = function(facebookID, extendedProfile){
		var basicProfile = Mutuality.getFriendOfFriendProfile(facebookID);
			if(basicProfile.location) {
				$("#profile-location").html('<i class="location"></i>' + basicProfile.location);
				$("#profile-location").attr('class', '');
			}
			else {
				$("#profile-location").html('<i class="location"></i>Location');
				$("#profile-location").attr('class', 'inactive');
			}
			if(extendedProfile.gender) {
				$("#profile-sex").html('<i class="male"></i>' + extendedProfile.gender);
				$("#profile-sex").attr('class', '');
			}
			else {
				$("#profile-sex").html('<i class="male"></i>Gender');
				$("#profile-sex").attr('class', 'inactive');			
			}
			if(extendedProfile.relationshipStatus) {
				$("#profile-status").html('<i class="single"></i>' + extendedProfile.relationshipStatus);
				$("#profile-status").attr('class', '');
			}
			else {
				$("#profile-status").html('<i class="single"></i>Relationship');
				$("#profile-status").attr('class', 'inactive');
			}
			if(extendedProfile.age) {
				$("#profile-dob").html('<i class="birthday"></i>' + extendedProfile.age);
				$("#profile-dob").attr('class', '');
			}
			else {
				$("#profile-dob").html('<i class="birthday"></i>Birthday');
				$("#profile-dob").attr('class', 'inactive');			
			}			
			if(extendedProfile.college) {
				$("#profile-education").html('<i class="edu"></i>' + extendedProfile.college);
				$("#profile-education").attr('class', '');
			}
			else {
				$("#profile-education").html('<i class="edu"></i>Education');
				$("#profile-education").attr('class', 'inactive');
			}
			if(extendedProfile.employer) {
				$("#profile-job").html('<i class="company"></i>' + extendedProfile.employer);
				$("#profile-job").attr('class', '');
			}
			else {
				$("#profile-job").html('<i class="company"></i>Job');
				$("#profile-job").attr('class', 'inactive');
			}

			$("#profile-stats ul").show();
			$("#profile-stats ul li").show();

			$(".profile-name").html(basicProfile.name);
			$("#profile-fb a").attr('onclick', Mutuality.getFacebookPageURL(basicProfile.facebookID));
	}

    // After AJAX call for getMeetPeople, load that into meet people page cache
    var meetPeopleSuccess = function(friends){
    	if (friends.length > 1){
    		console.log("Meet People Success = " + friends[2].facebookID)
    		fetchMeetPeopleProfileInfoAndShowUI(friends[2].facebookID, friends);
    	}
    }

    // Load the favorites into the UI
    var loadNewDataIntoCarousel = function (favorites){
    	$("#meet-profiles").html("");

    	for (i=0; i<MAX_CAROUSEL_NUM&&i<favorites.length; i++){
	    	var setFavoriteFunctionString = "Mutuality.setFavorite(" +favorites[i].facebookID+", function(success){ $('#add-to-fav').each(function(){ if ($(this).attr('facebookID') == favorites[i].facebookID){ $(this).css('background-position',  '0 -16px;'); }});});"    		
	    	var liElem = $('<li>', {class:'meet-profile', facebookID:favorites[i].facebookID}).appendTo(meetProfilesElem);
    		var aElem = $('<a>', {href:'#', class:"loaded"}).appendTo(liElem);
    		var imgElem = $('<img>', {src:Mutuality.getProfilePictureURL(favorites[i].facebookID, 350, 350)}).appendTo(aElem);
    		var spanElem = $('<span>', {class:"match-profile-details"}).appendTo(aElem);
    		var inFavorites = Mutuality.mpcache.favoritesList[favorites[i].facebookID];

    		if (!inFavorites) {
    			var spanElem2 = $('<span>', {id:"add-to-fav", class:"tooltip", title: "Add to Favorites", facebookID: favorites[i].facebookID, onclick:setFavoriteFunctionString}).appendTo(spanElem);
    		}
    		else{
    			var spanElem2 = $('<span>', {id:"add-to-fav", class:"tooltip", title: "Remove from Favorites", style:"background-position: 0 -16px;"}).appendTo(spanElem);
    			// console.log("yes a favorite");
    		}
    		var hElem = $('<h3>', {id:"left-profile-name", html:favorites[i].name}).appendTo(spanElem);
    	}

    	hideModal();
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
    var populateCTA = function(friends){
        friends.sort(function() { return 0.5 - Math.random();}) // shuffle the array
        $('#four-images img').each(function(i) {
            $(this).attr('src', Mutuality.getProfilePictureURL(friends[i].facebookID, 84, 84));
        });
    }
 /* End Helper Functions */

/* Begin Main Code */
   // Show the loading modal, and hide the page contents while async calls fire
   triggerModal();
   $("#main").hide();

   if($.cookie("UpdateFriendListCalled") !== "true") {
	    Mutuality.updateFriendList(0, function(){
	    	$.cookie("UpdateFriendListCalled", "true");
	   		Mutuality.loadFriendsList(populateCTA);
			Mutuality.getMeetPeople(0, 0, function(friends){
		    	Mutuality.mpcache.fofList = friends;
				meetPeopleSuccess(friends);
			});
			Mutuality.getFavoritesList(function(favorites){
				//console.log(favorites);
				for (i=0;i<favorites.length; i++){
					if (!Mutuality.mpcache.favoritesList[favorites[i].facebookID]) {
						Mutuality.mpcache.favoritesList[favorites[i].facebookID] = true;
					}
				}
			});
		});
	}
	else {
		Mutuality.loadFriendsList(populateCTA);
		Mutuality.getMeetPeople(0, 0, function(friends){
	    	Mutuality.mpcache.fofList = friends;
			meetPeopleSuccess(friends);
		});
		Mutuality.getFavoritesList(function(favorites){
			//console.log(favorites);
			for (i=0;i<favorites.length; i++){
				if (!Mutuality.mpcache.favoritesList[favorites[i].facebookID]) {
					Mutuality.mpcache.favoritesList[favorites[i].facebookID] = true;
				}
			}
		});
	}

	//Style adjustments
	$('#ask-about').css({ zIndex: 0 });
 
/* End Main Code */

})(jQuery);