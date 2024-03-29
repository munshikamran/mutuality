
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

    $("#register-button").click(function(){
        if($('#location-ajax').html() !== ""){
            $('#location-error').hide();
            var profileDict = {};
            profileDict['location'] = $("#reg-location").val();
            profileDict['relationship_status'] = $("#reg-relationship :selected").text();
            profileDict['gender'] = $("#reg-sex :selected").text();
            //console.log(profileDict);
            Mutuality.setProfile(profileDict['location'], profileDict['relationship_status'], profileDict['gender'], function(response){
                mixpanel.alias(Mutuality.cache.profile.facebookID);
                //mixpanel.identify(Mutuality.cache.profile.facebookID);
                mixpanel.track("Registration", {}, function() {
                    $('.success-trigger').trigger('click');
                    window.location = "/beacon/";
                });
            });
        }
        else {
            $('#location-error').show();
            $('.error-trigger').trigger('click');
        }
    });

    /* End Main Code */

})(jQuery);