(function($){

   var thumbRate = function(e, thumbsUp)
   {
       if(thumbsUp)
       {
           Mutuality.rateMatchThumbsUp(function(){
               var leftFriend  = Mutuality.getFriendProfile( Mutuality.cache.current[0] );
               var rightFriend = Mutuality.getFriendProfile( Mutuality.cache.current[1] );
               var leftimgURL = Mutuality.getProfilePictureURL(Mutuality.cache.current[0], 165, 165);
               var rightimgURL = Mutuality.getProfilePictureURL(Mutuality.cache.current[1], 165, 165);
               var leftName = leftFriend.name.split(" ")[0]
               var rightName = rightFriend.name.split(" ")[0]
               var headerLeft = "You should meet " + rightName + " on Mutuality"
               var headerRight = "You should meet " + leftName + " on Mutuality"
               var description =  "Everyone on Mutuality is a friend-of-a-friend. Mutuality (finally) makes meeting cool people safe and simple."
               var leftNudgeURL= Mutuality.getSendNudgeURL(this.cache.facebookID, leftFriend.facebookID, headerLeft, "http://www.mymutuality.com/makematches", "http://i.imgur.com/Hcy3Clo.jpg", description);
               var rightNudgeURL= Mutuality.getSendNudgeURL(this.cache.facebookID, rightFriend.facebookID, headerRight, "http://www.mymutuality.com/makematches", "http://i.imgur.com/Hcy3Clo.jpg", description);

               $('#nudge-left .match-name').text( leftFriend.name.split(" ")[0] );
               $('#nudge-left .introduce-thumb').css({backgroundImage: 'url('+leftimgURL+')'});
               $('#nudge-left .introduce-thumb').attr('onclick', leftNudgeURL);

               $('#nudge-right .match-name').text( rightFriend.name.split(" ")[0] );
               $('#nudge-right .introduce-thumb').css({backgroundImage: 'url('+rightimgURL+')'});
               $('#nudge-right .introduce-thumb').attr('onclick', rightNudgeURL);

               $('#nudge-both .introduce-thumb:eq(1)').css({backgroundImage: 'url('+leftimgURL+')'});
               $('#nudge-both .introduce-thumb:eq(0)').css({backgroundImage: 'url('+rightimgURL+')'});

               $("#rating-success").fadeIn(200, function() {
                       $("#rating-success").delay(2000).fadeOut(200, function() {
                           $("#rating-buttons").fadeIn(200);
                           $("#random-button").removeClass('disabled');
                       });
                });
           });
       }
       // else {
        
          // }
           // var reasons = new Array();
           // var subject  = Mutuality.cache.current[0];
           // var object = Mutuality.cache.current[1];
           // reasons.push({enum: "TOO_FAR", subject: subject, object: object}); // Temporary reason
           // Mutuality.rateMatchThumbsDown(reasons, function(){
           //         $("#rating-success").fadeIn(200, function() {
           //             $("#rating-success").delay(2000).fadeOut(200, function() {
           //                 $("#rating-buttons").fadeIn(200);
           //                 $("#random-button").removeClass('disabled');
           //                 $("#random-button").trigger('click');
           //             });
           //         });
           // });
       // }

   };

   $('#reason-select').bind('change', function (e){
       var currentReason = e.currentTarget.value;
       var isFound = false;
       $('#reason-list li').each(function() {
           var alreadyIncludedReason = $(this).context.childNodes[1].nodeValue.trim();
           if (alreadyIncludedReason.indexOf(currentReason) !== -1){
            isFound = true;
            }
       });
       console.log(isFound);
       if (!isFound && currentReason != ""){
        var htmlSnippet = '<li id="reason" class="alert-box secondary"><a href="#" class="close"> </a> ' + currentReason +' </li>'
        $("#reason-list").append(htmlSnippet);
       }
   });

   var matchLock = function(e)
   {
		var text = $(this).text() == "Unlocked" ? "Locked" : "Unlocked";
		$(this).text(text).toggleClass("locked");		
		return false;      
   }
   
	// Thumbs down
	$("#rating-down").bind('click', function(e) {	   
	  e.preventDefault();
    mixpanel.track("Match rated",{"Rating":"Down"})
	 if ($('#random-button').attr('class') !== "disabled"){
      $('#random-button').attr('class', 'disabled');
      var leftSex = $("#left-match-sex").val() == "Guys" ? 'male' : 'female';
      var rightSex = $("#right-match-sex").val() == "Guys" ? 'male' : 'female';
      Mutuality.loadNewMatch(leftSex, rightSex, Mutuality.cache.leftSlotLocked, Mutuality.cache.rightSlotLocked, matchSuccess);
  }
    // $("#rating-buttons").fadeOut(200, function() {
  //     $("#random-button").attr('class', 'disabled');
  //     thumbRate.call(this,e, false);
		// });
	});
	
	// Thumbs up
	$('#rating-up').bind('click', function(e){
	   e.preventDefault();
     mixpanel.track("Match rated",{"Rating":"Up"})
	   $("#rating-buttons").fadeOut(200, function() {
      $("#random-button").attr('class', 'disabled');
      thumbRate.call(this,e, true);
    });   
	});

  // Left lock button pressed
	$('#left-match-lock').bind('click', function(e){
	   e.preventDefault();
       if(!Mutuality.cache.rightSlotLocked){
        Mutuality.lockLeft();
	    matchLock.call(this,e);
       }
       else{
        Mutuality.lockRight();
        Mutuality.lockLeft();
        matchLock.call(this,e);
        matchLock.call($('#right-match-lock'),e);
       }
	});

  // Right lock button pressed
	$('#right-match-lock').bind('click', function(e){
	   e.preventDefault();
       if(!Mutuality.cache.leftSlotLocked){
        Mutuality.lockRight();
	    matchLock.call(this,e);
       }
       else{
        Mutuality.lockRight();
        Mutuality.lockLeft();
        matchLock.call(this,e);
        matchLock.call($('#left-match-lock'),e);
       }
	});
	
	
	$('#left-match-sex').bind('change', function(e){
        if(Mutuality.cache.leftSlotLocked){
            Mutuality.lockLeft();
            matchLock.call($('#left-match-lock'),e);
        }
        var leftSex = $("#left-match-sex").val() == "Guys" ? 'male' : 'female';
        var rightSex = $("#right-match-sex").val() == "Guys" ? 'male' : 'female';
        Mutuality.loadNewMatch(leftSex, rightSex, Mutuality.cache.leftSlotLocked, true, matchSuccess);
	});
	
	$('#right-match-sex').bind('change', function(e){
        if(Mutuality.cache.rightSlotLocked){
            Mutuality.lockRight();
            matchLock.call($('#right-match-lock'),e);
        }
        var leftSex = $("#left-match-sex").val() == "Guys" ? 'male' : 'female';
        var rightSex = $("#right-match-sex").val() == "Guys" ? 'male' : 'female';
        Mutuality.loadNewMatch(leftSex, rightSex, true, Mutuality.cache.rightSlotLocked, matchSuccess);
	});

  $(".search-box").live("blur", function(){
        var default_value = $(this).attr("rel");
        if ($(this).val() == ""){
                $(this).val(default_value);
        }
  }).live("focus", function(){
        var default_value = $(this).attr("rel");
        if ($(this).val() == default_value){
                $(this).val("");
        }
  });


    // Put in the search results into the DOM with actual search data
    var populateSearchResults = function(matches, parentID){
        $("#" + parentID +" .search-results li img").each(function(i){
            if(i < matches.length){
                $(this).css('display', '');
                $(this).attr('src', Mutuality.getProfilePictureURL(matches[i][0].facebookID));
            }
            else{
                $(this).css('display', 'none');
            }
        });
        $("#" + parentID +" .search-results li strong").each(function(i){
            if(i < matches.length){
                $(this).css('display', '');
                $(this).text(matches[i][0].name);
                $(this).data('facebookID', { facebookID: matches[i][0].facebookID });
                $(this).data('name', { name: matches[i][0].name });
                $(this).data('location', { location: matches[i][0].location });
            }
            else{
                $(this).css('display', 'none');
            }
        });
    }

	// Search input on Make Matches
	$(".search-box").keyup( function() {
        var parentID = $(this).parent().attr('id');
        var searchText = $("#" + parentID + " .search-box").val();
        var dropDownSex = $("#left-match-sex").val() == "Guys" ? "male" : "female";
        if (parentID.indexOf("right") != -1){
            dropDownSex = $("#right-match-sex").val() == "Guys" ? "male" : "female";
        }
        var matches = new Array();
        var rg = new RegExp(searchText,'i');
        if(Mutuality.cache.friends != null){
            $(Mutuality.cache.friends).each(function(){
                if($.trim($(this)[0].name).search(rg) != -1 && $(this)[0].gender == dropDownSex) {
                    if(matches.length < 3){
                        matches.push($(this));
                    }
                }
            });
            populateSearchResults(matches, parentID);
            $(this).siblings(".search-results").fadeIn(200);
        }
	});

    $(".search-results li a").bind('click', function(e) {
        console.log($(this));
        var parentID = $(this).parents("div").attr('id');
        console.log(parentID);
        var side = parentID.indexOf("right") != -1 ? "right" : "left";
        var name = $(this).find('strong').data('name')['name'];
        var facebookID = $(this).find('strong').data('facebookID')['facebookID'];
        var location = $(this).find('strong').data('location')['location'];
        var imgURL = Mutuality.getProfilePictureURL(facebookID, 350, 350);

        var friend = $('#'+side+'-match-profiles');

        $('img', friend).hide().attr('src', imgURL).parents('a').addClass('loaded');
        $('.profile-name', friend).text( name );
        if (location) {
            $('.profile-location', friend).attr( 'title', location );
        }
        else {
            $('.profile-location', friend).removeAttr( 'title');
        }
        $('img', friend).fadeIn(400);

        if(side == "right"){
            Mutuality.cache.current[1] = facebookID;
        }
        else{
            Mutuality.cache.current[0] = facebookID
        }

    });

	$(".search-box").focusout( function() {
		$(this).siblings(".search-results").fadeOut(200);
	});

    // When the spin button is clicked, load a new match!
    $('#random-button').bind('click', function(e){
        if ($(this).attr('class') !== "disabled"){
            $(this).attr('class', 'disabled');
            var leftSex = $("#left-match-sex").val() == "Guys" ? 'male' : 'female';
            var rightSex = $("#right-match-sex").val() == "Guys" ? 'male' : 'female';
            Mutuality.loadNewMatch(leftSex, rightSex, Mutuality.cache.leftSlotLocked, Mutuality.cache.rightSlotLocked, matchSuccess);
             mixpanel.track("Spin button clicked"); 
        }
    });

    // After AJAX call for new match, load the data into the UI
    var matchSuccess = function(match){
        $("#random-button").attr('class', '');
        var leftFriend   = $('#left-match-profiles');
        var rightFriend  = $('#right-match-profiles');
        if (match.length == 2) {
            var leftPerson = match[0];
            var rightPerson = match[1];
            var leftChanged = leftPerson.facebookID !== Mutuality.cache.current[0];
            var rightChanged = rightPerson.facebookID !== Mutuality.cache.current[1];

            Mutuality.cache.current = [leftPerson.facebookID, rightPerson.facebookID];

            $('#reason-container input:eq(0)').val( leftPerson.facebookID );
            $('#reason-container input:eq(1)').val( rightPerson.facebookID );

            // write all values to their elements
            if (leftChanged){
                leftPerson.image = Mutuality.getProfilePictureURL(leftPerson.facebookID, 350, 350);
                $('img', leftFriend).hide().attr('src', leftPerson.image).parents('a').addClass('loaded');
                $('.profile-name', leftFriend).text( leftPerson.name );
                $('.profile-name', leftFriend).attr( 'onclick', Mutuality.getFacebookPageURL(leftPerson.facebookID) );
                if (leftPerson.location) {
                    $('.profile-location', leftFriend).attr( 'title', leftPerson.location );
                }
                else {
                    $('.profile-location', leftFriend).removeAttr('title');
                }

                $('img', leftFriend).fadeIn(400);
            }

           if (rightChanged){
               rightPerson.image = Mutuality.getProfilePictureURL(rightPerson.facebookID, 350, 350);
               $('img', rightFriend).hide().attr('src', rightPerson.image).parents('a').addClass('loaded');
               $('.profile-name', rightFriend).text( rightPerson.name );
               $('.profile-name', rightFriend).attr( 'onclick', Mutuality.getFacebookPageURL(rightPerson.facebookID) );
                if (rightPerson.location) {
                    $('.profile-location', rightFriend).attr( 'title', rightPerson.location );
                }
                else {
                    $('.profile-location', rightFriend).removeAttr('title');
                }

               $('img', rightFriend).fadeIn(400);
           }

          $('.tooltip').tooltipster();
          $('.gender-question').tooltipster({
            theme:'.tooltipster-question',
            maxWidth:150,
            position:'top-left'
          });
          $('.lock-question').tooltipster({
            theme:'.tooltipster-question',
            maxWidth:150,
            position:'top-right'
          });
           $('.search-question').tooltipster({
            theme:'.tooltipster-question',
            maxWidth:150,
            position:'bottom-left'
          });

        }

    };

    // After AJAX call for finding friends of friends, load random four images into meet people call to action
    var friendsOfFriendsSuccess = function(friends){
        if (friends.length > 0){
            friends.sort(function() { return 0.5 - Math.random();}) // shuffle the array
            $('#four-images img').each(function(i) {
              if (i < friends.length) {
                $(this).attr('src', Mutuality.getProfilePictureURL(friends[i].facebookID, 84, 84));
              }
            });
        }
        else{
            $("#meet-people-cta").css('display','none');
        }
    };

   // Load friendslist and friends of friends via AJAX and populate the left and right
   // slots with a random match if the call already hasn't been made
    Mutuality.loadFriendsList(0, function(){});
    Mutuality.getMeetPeople(0, 0, 0, friendsOfFriendsSuccess);
    Mutuality.loadNewMatch('male', 'female', Mutuality.cache.leftSlotLocked, Mutuality.cache.rightSlotLocked, matchSuccess);
    
})(jQuery);
