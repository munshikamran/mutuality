
(function($) {

	// Initialize ajax autocomplete:
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

	//Sometimes getProfile takes a moment to return, so we should wait
	setTimeout(function(){
		if(Mutuality.cache.profile){
			if(Mutuality.cache.profile.gender == 'female'){
				$("#reg-sex a").eq(0).attr('class', 'selector');
				$("#reg-sex a").eq(0).html("");
				$("#reg-sex a").eq(1).attr('class', 'current');
				$("#reg-sex a").eq(1).html("Female");
			}


	$("#save-button").click(function(){
		if($('#location-ajax').html() !== ""){
			$('#location-error').hide();
			var profileDict = {};
			profileDict['location'] = $("#reg-location").val();
			profileDict['relationship_status'] = $("#reg-relationship :selected").text();
			profileDict['gender'] = $("#reg-sex :selected").text();
			console.log(profileDict);
			Mutuality.setProfile(profileDict['location'], profileDict['relationship_status'], profileDict['gender'], function(response){
				$('.success-trigger').trigger('click');
	            var url = window.location.href; 
				if(url.indexOf("register") !== -1) { 
					mixpanel.track("Registration");
					mixpanel.alias(Mutuality.cache.profile.facebookID);
					mixpanel.identify(Mutuality.cache.profile.facebookID);
					window.location = "/meetpeople/";

			if(Mutuality.cache.profile.relationshipStatus !== null){
				if(Mutuality.cache.profile.relationshipStatus.indexOf("Relationship") !== -1){
					$("#reg-relationship a").eq(0).attr('class', 'selector');
					$("#reg-relationship a").eq(0).html("");
					$("#reg-relationship a").eq(1).attr('class', 'current');
					$("#reg-relationship a").eq(1).html("In a Relationship");
				}
			}

			$("#reg-firstname").val(Mutuality.cache.profile.name);
			$("#reg-location").val(Mutuality.cache.profile.location);
			$("#location-ajax").html(Mutuality.cache.profile.location);
		}

		$("#save-button").click(function(){
			if($('#location-ajax').html() !== ""){
				$('#location-error').hide();
				var profileDict = {};
				profileDict['location'] = $("#reg-location").val();
				profileDict['relationship_status'] = $("#reg-relationship :selected").text();
				profileDict['gender'] = $("#reg-sex :selected").text();
				console.log(profileDict);
				Mutuality.setProfile(profileDict['location'], profileDict['relationship_status'], profileDict['gender'], function(response){
					$('.success-trigger').trigger('click');
		            var url = window.location.href; 
					if(url.indexOf("register") !== -1) { 
						mixpanel.track("Registration");
						mixpanel.alias(Mutuality.cache.profile.facebookID);
						mixpanel.identify(Mutuality.cache.profile.facebookID);
						window.location = "/meetpeople/";
					}
				});
			}
			else{
				$('#location-error').show();
				$('.error-trigger').trigger('click');
			}
		});  
	}, 100);
/* End Main Code */

})(jQuery);