
(function($) {

    function loadPage() {
        var friendNumber = calculateNumberOfFriends(2,5);
        Mutuality.getGoodFriends(friendNumber, function(goodFriendsObject) {
            console.log(goodFriendsObject);
            addFriendDiv(friendNumber, goodFriendsObject);
            addMatchNumber(friendNumber, goodFriendsObject.numPotentialMatches, goodFriendsObject.numFriends);
        });
    }

    function addFriendDiv (friendNumber, goodFriendsObject) {
        for (i = 0; i < friendNumber; i++) {
            
            $('#friend-list').append(
                $('<div>', {
                    class: "row"
                }));
            
            var twoColumns = $('<div>', {class:"two columns"});
            var threeColumns = $('<div>', {class:"three columns"});
            var sevenColumns = $('<div>', {class:"seven columns"});
            $('#friend-list').find('.row').last().append(threeColumns, twoColumns, sevenColumns);

            $('#friend-list').find('.row').last().find('.three').append($('<span>', {
                class:"share-friend-number",
                html:"+"
            }).append('<span class="share-number" id="share-friend-number-' + i +'">' + goodFriendsObject.goodFriends[i].friendIncrease + '</span> Matches' 
            ));

            var innerDiv = $('<div>',{class:"onoffswitch-inner"});
            var switchDiv = $('<div>',{class:"onoffswitch-switch"});
            var onOffSwitch = $('<input>', {type:"checkbox", name:"onoffswitch", id:"onoffswitch" + i, class:"onoffswitch-checkbox", checked:true});
            var onOffSwitchLabel = $('<label>', {class:"onoffswitch-label", for:"onoffswitch" + i}).append(innerDiv, switchDiv);
            $('#friend-list').find('.row').last().find('.two').append($('<div>', {class:"onoffswitch"}).append(onOffSwitch, onOffSwitchLabel));

            $('#friend-list').find('.row').last().find('.seven').append($('<label>', {
                class:"share-name",
                for: "onoffswitch",
                html: goodFriendsObject.goodFriends[i].name
            }));
        }

        $('.onoffswitch-checkbox').on('click', function() {
        var checkboxBoolean = $(this).is(':checked');
        if (checkboxBoolean === false) {
            var newFriendNumber = $(this).closest('.row').find('.share-number').html();
            $(this).closest('.row').find('.share-number').attr('data-friends', newFriendNumber);
            $(this).closest('.row').find('.share-number').html("0");
        } 
        else {
            $(this).closest('.row').find('.share-number').html($(this).closest('.row').find('.share-number').data("friends"));
        }
        addMatchNumber(friendNumber, goodFriendsObject.numPotentialMatches, goodFriendsObject.numFriends, function(){
                // var friendTotal = parseInt($('#share-friend-total').html());
                // if(friendTotal === 0) {
                //     alert("working");
                // }
            });
        });

        $('.invite.button').on('click', function(){
        var currentPersonName = Mutuality.getFriendOfFriendProfile(Mutuality.mpcache.current);
        var messageStringIntro = "Hey can you introduce me to " + currentPersonName.name + "?";
        var messageStringAsk = "Can you tell me more about " + currentPersonName.name + "?";
        var description = "Everyone on Mutuality is a friend-of-a-friend. Mutuality (finally) makes meeting cool people safe and simple.";

        Mutuality.getSendNudgeURL(Mutuality.cache.facebookID, mutualFriends[i].facebookID, messageStringAsk, "www.mymutuality.com?src=meetPeople_askAbout", "http://i.imgur.com/Hcy3Clo.jpg", description, [redirect]);

        });
    }
//var liElem = $('<li>', {class:'meet-profile', facebookID:friends[i].facebookID}).appendTo(meetProfilesElem);
//                        var aElem = $('<a>', {class:"loaded"}).appendTo(liElem);
//                        var imgElem = $('<img>', {src:Mutuality.getProfilePictureURL(friends[i].facebookID, 350, 350)}).appendTo(aElem);
//                        var spanElem = $('<span>', {class:"match-profile-details"}).appendTo(aElem);
//                        var inFavorites = friends[i].isFavorite;

    function calculateNumberOfFriends(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function addMatchNumber(friendNumber, numMatches, numFriends) {
        console.log(friendNumber);
        var total = 0;
        for (i = 0; i < friendNumber; i++) {
            currentID = "#share-friend-number-" + i;
            //console.log(currentID);
            var currentNumber = parseInt($(currentID).html());
            total = total +  currentNumber;
        }

        var totalConnectionsPossible = numFriends * 10;
        var totalNumberOfConnections = numMatches + total;
        var networkPercentage = Math.round((totalNumberOfConnections/totalConnectionsPossible)*100);

        //console.log(total);

        $('#share-friend-total').html(total);
        $('#network-percentage').html(networkPercentage);
        $('#progress-bar span').css("width",networkPercentage + "%");
    }

    /* End Helper functions */
   
    /* Begin Account Main Code */

    $(document).ready(function() {  
        loadPage();
    });

    $(window).load(function() {
      
    });

    /* End Main Code */

})(jQuery);