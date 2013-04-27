
(function($) {

	// Initialize ajax autocomplete for locations:
	$('#reg-location').autocomplete({
		serviceUrl: 'https://graph.facebook.com/search?type=adcity&limit=5&country_list=%5B"us"%5D',
		onSelect: function(suggestion) {
		    $('#location-ajax').html(suggestion.value);

		},
		deferRequestBy: 10,
		autoSelectFirst: true,
		onSearchStart: function (query) {$('#location-ajax').html("");},
		paramName: 'q',
		transformResult: function(response, originalQuery) {
		    return {
		        query: originalQuery,
		        suggestions: $.map(JSON.parse(response).data, function(dataItem) {
		            return { value: dataItem.name, data: dataItem.name };
		        })
		    };
		}
	});

    // Initialize ajax autocomplete for beacon places:
	$('#reg-place').autocomplete({
		serviceUrl: 'https://graph.facebook.com/search?type=place&fields=name',
		deferRequestBy: 10,
		autoSelectFirst: true,
        params: {access_token: $("#auth_token").html(), center:$("#lat").html() + "," + $("#long").html()},
		paramName: 'q',
		transformResult: function(response, originalQuery) {
		    return {
		        query: originalQuery,
		        suggestions: $.map(JSON.parse(response).data, function(dataItem) {
		            return { value: dataItem.name, data: dataItem.name };
		        })
		    };
		}
	});

    // Functions to get browser's current location
    function get_location() {
      navigator.geolocation.getCurrentPosition(print_coords);
    }

    function print_coords(position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;
      console.log(latitude);
      // let's show a map or do something interesting!
    }

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

	$('#reg-activity').tooltipster({
					theme: '.tooltipster-beacon',
					position: 'right',
					arrow:true,
					arrowColor:'#056ba6',
					maxWidth:300,
					trigger:'hover'
				}); 

	$('#reg-place').tooltipster({
					theme: '.tooltipster-beacon',
					position: 'right',
					arrow:true,
					arrowColor:'#056ba6',
					maxWidth:300,
					trigger:'hover'
				}); 

	// Show message
	for(var i=0;i<myMessages.length;i++){
		showMessage(myMessages[i]);
	}

	// When message is clicked, hide it
	$('.message').click(function(){			  
		  $(this).animate({top: -$(this).outerHeight()}, 300);
	});	

        $("#save-button").click(function(){
                var profileDict = {};

                profileDict['beacon-activity'] = $('#reg-activity').val();
                profileDict['beacon-place']  = $('#reg-place').val();
                Mutuality.setBeacon(profileDict['beacon-place'], profileDict['beacon-activity'], function(success){
                     $('.success-trigger').trigger('click');
                     setTimeout(function(){window.location="/meetpeople/";}, 200);
                }, function(fail){
                    $('#location-error').show();
                    $('.error-trigger').trigger('click');
                });
        });

		$('#reg-activity').on('focus', function(){
			$(this).tooltipster('show'); 
		});

		$('#reg-place').on('focus', function(){
			$(this).tooltipster('show'); 
		});

		$('.activity-list').on("click", 'a', function(){
			var activityName = $(this).html();
			$.scrollTo('input#reg-activity', 400);
			if (activityName !== "Other...") {
				var tooltipTitle = '<div id="beacon-activity-tooltip"><span class=beacon-info>Keep or edit this activity</span></div>';
				$('#reg-activity').tooltipster('update', tooltipTitle);
				$('input#reg-activity').val(activityName);
			} else {
				var tooltipTitleOther = '<div id="beacon-activity-tooltip"><span class=beacon-info>Add your own activity</span></div>';
				//$('input#reg-activity').attr('title', tooltipTitle);
				$('#reg-activity').tooltipster('update',tooltipTitleOther); 
				$('input#reg-activity').val("");
				//$('input#reg-activity').click();
			}
			$('#reg-activity').focus();
		})

/* End Main Code */

})(jQuery);