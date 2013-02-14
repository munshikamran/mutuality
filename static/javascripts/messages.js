
(function($) {
/* Begin Helper functions */

	//Load thread previews into the UI
	var loadThreadPreviewsIntoUI = function (messages){
		console.log(messages);
		messageListUl = $(".message-list ul")

		for (var i = 0; i < messages.length; i++){
			console.log(messages.length);
			var liElem = $('<li>', {class:'cf inactive', facebookID:messages[i].sender}).appendTo(messageListUl);
    		var aElem = $('<a>', {href:'#'}).appendTo(liElem);
    		var spanElemStyle = "background-image:" + Mutuality.getProfilePictureURL(messages[i].sender, 45, 45);
    		var spanElem = $('<span>', {class:"profile-thumb", style: spanElemStyle}).appendTo(aElem);
    		var strongElem = $('<strong>', {class:""}).appendTo(aElem);
    		var smallElem = $('<small>', {class:""}).appendTo(aElem);
		}
	}

	//Mutuality.getFriendOfFriendProfile(messages[i].sender).name
	//text: messages[i].sent_at

/* End Helper functions */

/* Begin Messages Main Code */


	// Get Thread Previews
	Mutuality.getThreadPreviews(loadThreadPreviewsIntoUI);


   
/* End Main Code */

})(jQuery);