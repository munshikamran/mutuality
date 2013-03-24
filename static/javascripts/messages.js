
(function($) {

/* Begin Helper functions */
// After AJAX call for finding friends of friends, load random four images into meet people call to action

/*
var friendsOfFriendsSuccess = function(friends){
        if (friends.length > 0){
        	console.log("working");
            friends.sort(function() { return 0.5 - Math.random();}) // shuffle the array
            $('#four-images img').each(function(i) {
                $(this).attr('src', Mutuality.getProfilePictureURL(friends[i].facebookID, 84, 84));
            });
        }
        else{
            $("#meet-people-cta").css('display','none');
        }
};

*/
function formatTime (dateString) {
	
	var a_p = "";
	var d = new Date(dateString);
	var curr_hour = d.getHours();

	if (curr_hour < 12) {
			a_p = "AM";
   		} else {
   			a_p = "PM";
   		}
	if (curr_hour == 0) {
   		curr_hour = 12;
   		}
	if (curr_hour > 12) {
   		curr_hour = curr_hour - 12;
   	}

var curr_min = d.getMinutes();
	if (curr_min < 10) {
		curr_min = "0" + curr_min;
	}

return curr_hour + ":" + curr_min + " " + a_p;
}

var initAskAboutCarousel = function () {
		$('.ask-about').carouFredSel({
			auto : false,
			width: 213,
			height: 110,
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
	};



//Load full message exchange into the UI
var loadMessageThreadIntoUI = function(messageThread) {
	var totalHeight = 0;
	var messageHeight = 0;
	var messagePos;
		if ($('.single-message').length === 0) {
			messagePos = messageThread.length - 1;
		} else {
			messagePos = $('.single-message').eq(0).data('messageposition');
		}
	for (var i = messagePos; i >= 0; i--) {
		var messageOwner = messageThread[i].sender.facebookID;
		var thumbImage = 'background-image: url(' + Mutuality.getProfilePictureURL(messageOwner, 45, 45) + ')';
		var time = formatTime(messageThread[i].sent_at);
		//console.log(time);
		//console.log($('.single-message').length);	
			if ($('.single-message').length !== 0) { 
				messageHeight = $('.single-message').eq(0).height();
				//console.log(messageHeight);
				totalHeight = totalHeight + messageHeight;
				//console.log(totalHeight);
			}
		if (totalHeight < 400 || i === messagePos) {
		$('.message-thread').prepend(
			$('<div>').addClass('single-message row').append(
				$('<div>').addClass('two columns').append(
					$('<span>').attr({
						class: "profile-thumb",
						style:  thumbImage,
					}), 
					($('<small>').html(time))
					)).append(
					($('<div>').addClass('ten columns').html(
						"<p>" + messageThread[i].body + "</p>"	
						)
						)));
			} else {
				$('.single-message').eq(0).attr({
						'data-messageposition': i,
					});
				$('.message-thread').prepend('<div class="load-messages row"><a href="#">Load previous messages</a></div>');
				break;
			}
		}
	}

var loadSentMessage = function(messageThread) {
	var sentMessage = messageThread[messageThread.length-1];
	var messageOwner = sentMessage.sender.facebookID;
	var thumbImage = 'background-image: url(' + Mutuality.getProfilePictureURL(messageOwner, 45, 45) + ')';
	var time = formatTime(sentMessage.sent_at);
	var newMessagePos = $('.single-message').eq(0).data('messageposition') + 1;
	var messageAdded = false;
	if ($('.message-thread').height() > 450) {
		$('.single-message').eq(0).remove();
		messsageAdded = true;
	}
	
	$('.message-thread').append(
		$('<div>').addClass('single-message row').append(
			$('<div>').addClass('two columns').append(
					$('<span>').attr({
						class: "profile-thumb",
						style:  thumbImage,
					}), 
					($('<small>').html(time))
					)).append(
					($('<div>').addClass('ten columns').html(
						"<p>" + sentMessage.body + "</p>"	
						)
						)))
	if (messageAdded = true) {
		$('.single-message').eq(0).attr('data-messageposition',newMessagePos);
	}
}

//Load thread previews into the UI
var loadThreadPreviewsIntoUI = function (messages) {
			if (messages[0].sender.facebookID !== Mutuality.token) {
				var loadFirstPerson = messages[0].sender.facebookID; 
			}
			else {
				var loadFirstPerson = messages[0].recipient.facebookID;
			}	
			$('.message-thread').empty();
			Mutuality.getMessagesWithOther(loadFirstPerson, loadMessageThreadIntoUI);
			Mutuality.getMutualFriendList(loadFirstPerson, function(mutualFriends) {
				loadMutualFriendsIntoUI(loadFirstPerson, messages[0].sender.name, mutualFriends);
				});

		for (var i = 0; i < messages.length; i++) {
			var otherPerson;
			if (messages[i].sender.facebookID !== Mutuality.token) {
				var otherPerson = messages[i].sender 
			}
			else {
				var otherPerson = messages[i].recipient;
			}
			//console.log(otherPerson);
			//messages[i].sender.facebookID;
			var profileImage = 'background-image: url(' + Mutuality.getProfilePictureURL(otherPerson.facebookID, 45, 45) + ')';
			var date = new Date(messages[i].sent_at);
			var formattedMessage;
			var messageBody = messages[i].body;
			if (messageBody.length < 30) {
				formattedMessage = messageBody;
			}
			else {
				formattedMessage = messageBody.substr(0,20) + "...";
			}
			var name = otherPerson.name;	
				
				//Add preview HTML element into DOM	
				$('.message-list ul').append(
					$('<li>').addClass(function() {
						if (i !== 0) {
							return 'cf inactive';
						} else {
							return 'cf active';
						}	
					})
					.append(
							$('<a>').attr('href','#').append(
								$('<span>').attr({
									class: "profile-thumb",
									style: profileImage,
									}),
								($('<strong>').html(name)),
								($('<small>').html(formattedMessage))
								)));
	
					$('.message-list ul li').eq(i).attr({
						'data-facebookid': otherPerson.facebookID,
						'data-name':otherPerson.name
					});
			}	
	}

	var loadMutualFriendsIntoUI = function (facebookID, otherName, mutualFriends){
		var name = otherName.split(" ");
		var newUlElem;
		$('.ask-about').empty();
		$('.profile-name').html("Ask About " + name[0]);
		for (var i = 0; i < mutualFriends.length; i++) {
			var friendID = mutualFriends[i].facebookID;
			var mutualFriendImage = 'background-image: url(' + Mutuality.getProfilePictureURL(friendID, 45, 45) + ')';
			if (i % 6 == 0){
				newUlElem = $('<ul>', {style: "margin-right: 0px;"}).appendTo($('.ask-about'));
				}
				var liElem = $(newUlElem).append
					($('<li>').append(
						$('<a>').attr('href','#').append(
							$('<span>').attr({
									class: "profile-thumb tooltip",
									title: "Ask " + mutualFriends[i].name.split(" ")[0],
									style: mutualFriendImage,
									}))));
			};
			$('.tooltip').tooltipster();
			initAskAboutCarousel();
	}

/* End Helper functions */

/* Begin Messages Main Code */

	// Get and show full message thread when relevant preview li element is clicked
	$(document).ready(function() {
	
		// Get Thread Previews
		Mutuality.getThreadPreviews(loadThreadPreviewsIntoUI);

		//Load overflow messages
		$(document).on('click', '.load-messages', function (event) { 
			event.stopPropagation();
			$(this).hide();
			$(".message-thread").css({"height":"400px", "width":"450px", "overflow-y":"scroll", "overflow-x":"hidden"});
			var otherFbId = $('.message-list').find('li.active').data('facebookid');
			Mutuality.getMessagesWithOther(otherFbId, loadMessageThreadIntoUI);
			//Mutuality.getMeetPeople(0, 0, friendsOfFriendsSuccess);
		});

		$('.message-list ul').on('click', 'li', function (event) {
			event.stopPropagation();
			event.preventDefault();
			$(this).siblings('li').removeClass("cf active").addClass("cf inactive");
			$(this).removeClass("cf inactive").addClass("cf active");
			var otherFbId = $('.message-list').find('li.active').data('facebookid');
			var otherName = $('.message-list').find('li.active').data('name');
			$('.message-thread').empty();
			//$(.'ask-about').empty();
			Mutuality.getMutualFriendList(otherFbId, function(mutualFriends){
				loadMutualFriendsIntoUI(otherFbId, otherName, mutualFriends);
			})
			Mutuality.getMessagesWithOther(otherFbId, loadMessageThreadIntoUI);	
		});

		//Send button sends message in message field
		$('input.messages.button').on('click', function (event){
			event.stopPropagation();
			var sendTo = $('.message-list').find('li.active').data('facebookid');
			//console.log(sendTo);
			var messageToSend = $('.message-reply').find('textarea').val();
			//console.log(messageToSend);
			Mutuality.sendMessage(sendTo, messageToSend, function(response){
				if (response === true) {
					var otherFbId = $('.message-list').find('li.active').data('facebookid');
					$('.message-reply').find('textarea').val("");
					Mutuality.getMessagesWithOther(otherFbId, loadSentMessage);
					//$('.message-thread').empty();
					//$('.message-thread').replaceWith(Mutuality.getMessagesWithOther(otherFbId, loadMessageThreadIntoUI));	
				} else {
				   alert("Error: can't send message");	
				}
			});
		});

		$('.message-reply').find('textarea').keypress(function(event) {
			event.stopPropagation();
			if (event.which === 13) {
				$('input.messages.button').click();
			}
		});	


	
	});
   
/* End Main Code */

})(jQuery);