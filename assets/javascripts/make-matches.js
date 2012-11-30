(function($){
   
   var thumbRate = function(e, thumbsUp)
   {      
	   var rateToken  = $('input[name=is]:checked').val();
	   var matchToken = $('input[name=is]:not(:checked)').val();
	   var reason     = $('#reason-select').val();

	   // make request to rate friend
	   // backed should take the rateToken which is for the
	   // selected friend and remove from the current list
	   // of matches for the matchToken friend if request is thumbsDown
	   Mutuality.rateFriend( matchToken, rateToken, reason, function(){
	      
	      var leftFriend  = Mutuality.getFriendProfile( Mutuality.cache.current[0] );
	      var rightFriend = Mutuality.getFriendProfile( Mutuality.cache.current[1] );

	      if(thumbsUp)
	      {
	         $('#nudge-left .match-name').text( leftFriend.full_name.split(/\s/).shift() );
	         $('#nudge-left .introduce-thumb').css({backgroundImage: 'url('+leftFriend.image+')'});
	         
	         $('#nudge-right .match-name').text( rightFriend.full_name.split(/\s/).shift() );
	         $('#nudge-right .introduce-thumb').css({backgroundImage: 'url('+rightFriend.image+')'});
	         
	         $('#nudge-both .introduce-thumb:eq(1)').css({backgroundImage: 'url('+leftFriend.image+')'});
	         $('#nudge-both .introduce-thumb:eq(0)').css({backgroundImage: 'url('+rightFriend.image+')'});
	      }
	      else
	      {
	         
         }	      
	   });
   };   
   
   
   var matchLock = function(e)
   {
		var text = $(this).text() == "Unlocked" ? "Locked" : "Unlocked";
		$(this).text(text).toggleClass("locked");		
		return false;      
   }
   
   var matchGender = function(e, side, exclude)
   {
      var exclude = exclude || '';
	  var gender = $(this).val() == 'Guys' ? 'male' : 'female';

	   // load gender matches
	   Mutuality.loadFriendsList( gender, function( friends ){
	      
         var list   = $('#'+side+'-match-profiles');
         var listArray  = friends[gender];
         var found = null;

         // remove exclusion from list
         // "Jane" can't date "Jane"
         for(var i=0,len = listArray.length;i<len;i++)
         {
            if(listArray[i].token == exclude)
            {
               listArray.splice( i, 1 );
               break;
            }
         }

         // yank a random friend
         var listRand  = listArray[Math.floor(Math.random() * listArray.length)];
         var listFriend  = $('li', list);

         // write current visible friends to cache and store as
         // values for thumb inputs
         
         if(side == 'left') 
         {
            Mutuality.cache.current[0] = listRand.token;
            $('#reason-container input:eq(0)').val( listRand.token );
         }
         else
         {
            Mutuality.cache.current[1] = listRand.token;
            $('#reason-container input:eq(1)').val( listRand.token );            
         }

         // write all values to their elements     
         $('img', listFriend).hide().attr('src', listRand.image).parents('a').addClass('loaded');
         $('.profile-name', listFriend).text( listRand.full_name );
         $('.profile-location', listFriend).text( listRand.city+', '+listRand.state );

         $('img', listFriend).fadeIn(750);
	   });
   }
   
	// thumbs up
	$("#rating-down").bind('click', function(e) {	   
	   e.preventDefault();
		$("#rating-buttons").fadeOut(200, function() {
			$("#reasons").fadeIn(200);
		});
	});
	
	// thumbs down
	$('#rating-up').bind('click', function(e){
	   e.preventDefault();
	   thumbRate.call(this,e, true);	   
	});
	
	// done rating (thumbs down only)
	$("#done-button").bind('click', function(e) {
	   e.preventDefault();
	   thumbRate.call(this,e, false);
		
		$("#reasons").fadeOut(200, function() {
			$("#rating-success").fadeIn(200, function() {
				$("#rating-success").delay(2000).fadeOut(200, function() {
					$("#rating-buttons").fadeIn(200);
				});
			});
		});
	});
	
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

	});
	
	$('#right-match-sex').bind('change', function(e){

	});

    // Put in the search results into the DOM with actual search data
    var populateSearchResults = function(matches, parentID){
        $("#" + parentID +" .search-results li span").each(function(i){
            console.log(matches.length);
            if(i < matches.length){
                var imgURL = "https://graph.facebook.com/" + matches[i][0].facebookID + "/picture";
                $(this).css('display', '');
                $(this).css('background-image', 'url('+imgURL+')');
            }
            else{
                $(this).css('display', 'none');
            }
        });
        $("#" + parentID +" .search-results li strong").each(function(i){
            if(i < matches.length){
                $(this).css('display', '');
                $(this).text(matches[i][0].name);
            }
            else{
                $(this).css('display', 'none');
            }
        });
    }
	// Search input on Make Matches
	$(".search-box").keyup( function() {
        parentID = $(this).parent().attr('id');
        searchText = $("#" + parentID + " .search-box").val();
        var matches = new Array();
        var rg = new RegExp(searchText,'i');
        if(Mutuality.cache.friends != null){
            $(Mutuality.cache.friends).each(function(){
                if($.trim($(this)[0].name).search(rg) != -1) {
                    if(matches.length < 3){
                        matches.push($(this));
                    }
                }
            });
            populateSearchResults(matches, parentID);
            $(this).siblings(".search-results").fadeIn(200);
        }
	});

	$(".search-box").focusout( function() {
		$(this).siblings(".search-results").fadeOut(200);
	});

    // When the spin button is clicked, load a new match!
    $('#random-button').bind('click', function(e){
        var leftSex = $("#left-match-sex").val() == "Guys" ? 'male' : 'female';
        var rightSex = $("#right-match-sex").val() == "Guys" ? 'male' : 'female';
        Mutuality.loadNewMatch(leftSex, rightSex, matchSuccess);
    });

    // After AJAX call for new match, load the data into the UI
    var matchSuccess = function(match){
        var leftFriend   = $('#left-match-profiles');
        var rightFriend  = $('#right-match-profiles');
        if (match.length == 2) {
            var leftPerson = match[0];
            var rightPerson = match[1];
            Mutuality.cache.current = [leftPerson.facebookID, rightPerson.facebookID];

            $('#reason-container input:eq(0)').val( leftPerson.facebookID );
            $('#reason-container input:eq(1)').val( rightPerson.facebookID );

            // write all values to their elements

            leftPerson.image = Mutuality.getProfilePictureURL(leftPerson.facebookID);
            $('img', leftFriend).hide().attr('src', leftPerson.image).parents('a').addClass('loaded');
            $('.profile-name', leftFriend).text( leftPerson.name );
            if (leftPerson.location) {
                $('.profile-location', leftFriend).text( leftPerson.location );
            }
            else {
                $('.profile-location', leftFriend).text("");
            }

           rightPerson.image = Mutuality.getProfilePictureURL(rightPerson.facebookID);
           $('img', rightFriend).hide().attr('src', rightPerson.image).parents('a').addClass('loaded');
            $('.profile-name', rightFriend).text( rightPerson.name );
            if (rightPerson.location) {
                $('.profile-location', rightFriend).text( rightPerson.location );
            }
            else {
                $('.profile-location', rightFriend).text("");
            }

            $('img', leftFriend).fadeIn(400);
            $('img', rightFriend).fadeIn(400);
        }

    };

   // Load friends via AJAX and populate the left and right
   // slots with a random match.
   Mutuality.loadFriendsList(null, function(){});
   Mutuality.loadNewMatch('male', 'female', matchSuccess);


})(jQuery);
