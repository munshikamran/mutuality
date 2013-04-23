
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
		serviceUrl: 'https://graph.facebook.com/search?type=place&distance=1000',
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

	// Show message
	for(var i=0;i<myMessages.length;i++){
		showMessage(myMessages[i]);
	}

	// When message is clicked, hide it
	$('.message').click(function(){			  
		  $(this).animate({top: -$(this).outerHeight()}, 300);
	});	

        $("#save-button").click(function(){
            if($('#location-ajax').html() !== ""){
                $('#location-error').hide();
                var profileDict = {};
                profileDict['location'] = $("#reg-location").val();
                profileDict['relationship_status'] = $("#reg-relationship :selected").text();
                profileDict['gender'] = $("#reg-sex :selected").text();
                profileDict['beacon-activity'] = $('#reg-activity').val();
                profileDict['beacon-place']  = $('#reg-place').val();
                Mutuality.setBeacon(profileDict['beacon-place'], profileDict['beacon-activity'], "category1", function(success){
                	console.log(success);
                });
                Mutuality.setProfile(profileDict['location'], profileDict['relationship_status'], profileDict['gender'], profileDict['beacon-activity'], profileDict['beacon-place'], function(response){
                     $('.success-trigger').trigger('click');
                 });
            }
            else {
                $('#location-error').show();
                $('.error-trigger').trigger('click');
            }
        });

/* End Main Code */

})(jQuery);