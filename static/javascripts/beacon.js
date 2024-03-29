
(function($) {

    // Initialize ajax autocomplete for beacon places:
	$('#reg-place').autocomplete({
		serviceUrl: 'https://graph.facebook.com/search?type=place&fields=name,location',
        onSelect: function(suggestion) {
            $('#places-ajax').html(suggestion.value);
            $('#places-error').hide();
            var graphURL = 'https://graph.facebook.com/fql?access_token='+ $("#auth_token").html() +'&q=SELECT name, page_id, categories, description, general_info, pic_big FROM page WHERE page_id IN (SELECT page_id, name FROM place WHERE  distance(latitude, longitude,"'+ suggestion.location.latitude +'", "'+ suggestion.location.longitude +'") < 10)';
            $.ajax({
                url: graphURL,
                dataType: 'json',
                type: 'GET',
                success: function(data) {
                    if (data.data.length !== 0){
                        $('#places-ajax').html(data.data[0].name);

                        $('#place-description img').attr('src', data.data[0].pic_big);
                        $('#place-description h4').html( data.data[0].name);
                    }
                    else{
                        $('#place-description img').attr('src', 'http://www.mymutuality.com/images/noPlace.png');
                        $('#place-description h4').html( $('#reg-place').val() );
                    }
                },
                error: function(data) {
                    console.log("error");
                }
		    });
        },
        onSearchStart: function (query) {$('#places-ajax').html("");},
		deferRequestBy: 10,
		autoSelectFirst: true,
        params: {access_token: $("#auth_token").html(), center:$("#lat").html() + "," + $("#long").html()},
		paramName: 'q',
		transformResult: function(response, originalQuery) {
		    return {
		        query: originalQuery,
		        suggestions: $.map(JSON.parse(response).data, function(dataItem) {
		            return { value: dataItem.name, data: dataItem.name, location: dataItem.location };
		        })
		    };
		}
	});

    $("#save-button").click(function(){
        if($('#places-ajax').html() !== "" && $("#reg-place").val() !== ""){
            var profileDict = {};
            profileDict['beacon-activity'] = $('#reg-activity').val();
            profileDict['beacon-place']  = $('#reg-place').val();
            Mutuality.setBeacon(profileDict['beacon-place'], profileDict['beacon-activity'], function(success){
                $('.success-trigger').trigger('click');
                setTimeout(function(){
                    FB.ui(
                        {
                           method: 'feed',
                           name: 'Anyone want to join me for ' + $('#reg-activity').val() + ' at ' + $('#reg-place').val() + '?',
                           link: $("#main").data('url'),
                         },
                      function(response) {
                        if (response && response.post_id) {
                          console.log('Post was published to facebook.');
                          mixpanel.track("Beacon set", {
                                "Activity": profileDict['beacon-activity'],
                                "Place": profileDict['beacon-place'],
                                "FacebookPosted": "true"}, function() {
                                window.location = '/meetpeople/';
                                });
                          

                        } else {
                          console.log('Post was not published to facebook.');
                          mixpanel.track("Beacon set", {
                                "Activity": profileDict['beacon-activity'],
                                "Place": profileDict['beacon-place'],
                                "FacebookPosted": "false"}, function() {
                                window.location = '/meetpeople/';
                                });
                        }
                      }
                    );
                },300);
            }, function(fail){
                $('#location-error').show();
                $('.error-trigger').trigger('click');
            });
        }
        else{
            $('#places-error').show();
            $('.error-trigger').trigger('click');
        }
    });

    $("#post-fb-button").click(function(){
        $("#save-button").trigger('click');
        var feedPostUrl = 'https://graph.facebook.com/me/feed/';
            $.ajax({
                url: feedPostUrl,
                dataType: 'json',
                type: 'POST',
                params: {access_token: $("#auth_token").html(),
                            message: "fuck yeah",
                            link: "google.com",
                            name: "hello",
                            caption: "caption",
                            description: "description"},
                success: function(data) {
                    console.log("success")
                },
                error: function(data) {
                    console.log("error");
                }
		    });
    });

    $('#reg-activity').on('focus', function(){
        $(this).tooltipster('show');
        if ( $('#reg-place').val().length > 0) {
                $('#place-description').animate({width:'hide'},350, function(){
                    $("#accordion").animate({width:'show'},350);
                });
            } else {
                $('#place-information').animate({width:'hide'},350, function(){
                    $("#accordion").animate({width:'show'},350);
                });
            }
    });

    $('#reg-place').on('focus', function(){
        $(this).tooltipster('show');
        $("#accordion").animate({width:'hide'},350, function(){
            if ( $('#reg-place').val().length > 0) {
                $('#place-description').animate({width:'show'},350);
            } else {
                $('#place-information').animate({width:'show'},350);
            }
        });
    });

    $('.activity-list').on("click", 'a', function(){
        var activityName = $(this).html();
        $.scrollTo('input#reg-activity', 400);
        if (activityName !== "Other...") {
            var tooltipTitle = '<div id="beacon-activity-tooltip"><span class=beacon-info>Keep or change this activity</span></div>';
            $('#reg-activity').tooltipster('update', tooltipTitle);
            $('input#reg-activity').val(activityName);
            //$('input#reg-activity').attr('disabled','disabled');
        } else {
            var tooltipTitleOther = '<div id="beacon-activity-tooltip"><span class=beacon-info>Add your own activity</span></div>';
            //$('input#reg-activity').attr('title', tooltipTitle);
            $('#reg-activity').tooltipster('update',tooltipTitleOther);
            $('input#reg-activity').val("");
            //$('input#reg-activity').removeAttr('disabled');
            //$('input#reg-activity').click();
        }
        $('#reg-activity').focus();
    });


/* Begin Helper functions */
	//Alert message stuff
	var myMessages = ['error','success']; // define the messages types		 
	var hideAllMessages = function() {
		 var messagesHeights = new Array(); // this array will store height for each
		 for (i=0; i<myMessages.length; i++) {
				  messagesHeights[i] = $('.' + myMessages[i]).outerHeight();
				  $('.' + myMessages[i]).css('top', -messagesHeights[i]); //move element outside viewport
		 }
	}

	var showMessage = function(type){
		$('.'+ type +'-trigger').click(function(){
			  hideAllMessages();				  
			  $('.'+type).animate({top:"0"}, 300);
			  setTimeout(function(){$('.'+type).animate({top: -$(this).outerHeight()}, 300)}, 1000);
		});
	}


/* End Helper functions */

/* Begin Account Main Code */

	// Initially, hide them all
	hideAllMessages();

	// Show message
	for(var i=0;i<myMessages.length;i++){
		showMessage(myMessages[i]);
	}

    $(document).ready(function(){
        setTimeout(function(){
            $('#accordion').animate({width:'show'},350);
            setTimeout(function(){
                 var randomNumber = Math.round(Math.random()*(2) + 1);
                $('#accordion').find('.link-header').eq(randomNumber).click();
            },500)
        },500);


    })

	// When message is clicked, hide it
	$('.message').click(function(){			  
		  $(this).animate({top: -$(this).outerHeight()}, 300);
	});

    // When page loads, check to see if a place is already filled in and populate the image from facebook.
    if($("#reg-place").val() !== ""){
        // First we need the lat/long of the place
        var serviceUrl= 'https://graph.facebook.com/search?type=place&fields=name,location&access_token='+$("#auth_token").html()+'&q="' + $("#reg-place").val() + '"';
        $.ajax({
                url: serviceUrl,
                dataType: 'json',
                type: 'GET',
                success: function(data) {
                    if (data.data.length !== 0){
                        // Once we have the lat/long we can get the pic
                        var graphURL = 'https://graph.facebook.com/fql?access_token='+ $("#auth_token").html() +'&q=SELECT name, page_id, categories, description, general_info, pic_big FROM page WHERE page_id IN (SELECT page_id, name FROM place WHERE  distance(latitude, longitude,"'+ data.data[0].location.latitude +'", "'+ data.data[0].location.longitude +'") < 10)';
                        $.ajax({
                            url: graphURL,
                            dataType: 'json',
                            type: 'GET',
                            success: function(response) {
                                if (response.data.length !== 0){
                                    $('#place-description img').attr('src', response.data[0].pic_big);
                                    $('#place-description h4').html(response.data[0].name);
                                }
                        },
                            error: function(data) {
                                console.log("error");
                            }
                        });
                    }
                },
                error: function(data) {
                    console.log("error");
                }
		    });
        }

        // After AJAX call for finding friends of friends, load random four images into meet people call to action
        var friendsOfFriendsSuccess = function(friends){
            var friends = friends.potentialMatches;
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

        Mutuality.getMeetPeople("FRIENDSHIP", friendsOfFriendsSuccess);


/* End Main Code */

})(jQuery);

