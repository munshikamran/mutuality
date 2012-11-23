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
	   if(Mutuality.cache.current.length == 0) return;
	   
	   e.preventDefault();
	   Mutuality.lockFriend( Mutuality.cache.current[0] );
	   matchLock.call(this,e);
	});
	
	$('#right-match-lock').bind('click', function(e){
	   if(Mutuality.cache.current.length == 0) return;
	   
	   e.preventDefault();
	   Mutuality.lockFriend( Mutuality.cache.current[1] );
	   matchLock.call(this,e);
	});
	
	
	$('#left-match-sex').bind('change', function(e){
	   
	   // passing the index of the opposite side
	   // to exclude them from the list
	   var exclude = Mutuality.cache.current[1];
	   matchGender.call(this, e, 'left', exclude);	   
	});
	
	$('#right-match-sex').bind('change', function(e){
	   
	   // passing the index of the opposite side
	   // to exclude them from the list
	   var exclude = Mutuality.cache.current[0];
	   matchGender.call(this, e, 'right', exclude);	   
	});
	
	// Thumbs up modal
	/* Is this used???????????
	$("#buttonForModal").click(function() {
		$("#myModal").reveal();
	});
	*/

	
	// Search input on Make Matches
	$(".search-box").keyup( function() {
		$(this).siblings(".search-results").fadeIn(200);
	});
	$(".search-box").focusout( function() {
		$(this).siblings(".search-results").fadeOut(200);
	});

	
   // load friends in via Ajax and populate the left and right
   // sides with a random friend. I assume random as the first
   // load will contain all friends
   Mutuality.loadFriendsList(null, function(friends){

     Mutuality.cache.friends = friends;

     var leftList   = $('#left-match-profiles');
     var rightList  = $('#right-match-profiles');     
     var leftArray  = friends.male;
     var rightArray = friends.female;
     
     // yank a random male and female friend
     var leftRand  = leftArray[Math.floor(Math.random() * leftArray.length)];
     var rightRand = rightArray[Math.floor(Math.random() * rightArray.length)];
     
     var leftFriend  = $('li', leftList);
     var rightFriend = $('li', rightList);
     
     // write current visible friends to cache and store as
     // values for thumb inputs
     Mutuality.cache.current = [ leftRand.token, rightRand.token ];
     
     $('#reason-container input:eq(0)').val( leftRand.token );
     $('#reason-container input:eq(1)').val( rightRand.token ); 
     
     // write all values to their elements     
     $('img', leftFriend).hide().attr('src', leftRand.image).parents('a').addClass('loaded');
     $('.profile-name', leftFriend).text( leftRand.full_name );
     $('.profile-location', leftFriend).text( leftRand.city+', '+leftRand.state );
     
     $('img', rightFriend).hide().attr('src', rightRand.image).parents('a').addClass('loaded');    
     $('.profile-name', rightFriend).text( rightRand.full_name );  
     $('.profile-location', rightFriend).text( rightRand.city+', '+rightRand.state );
     
     $('img', leftFriend).fadeIn(400);
     $('img', rightFriend).fadeIn(400);     
   });
	
})(jQuery);
