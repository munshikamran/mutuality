//
//  mutuality.js
//  Mutuality Main Library
//

///////////////////////////////////////
// Utility functions
///////////////////////////////////////

// Add method to Number for radian lookup
if (typeof(Number.prototype.toRad) === "undefined") {
   Number.prototype.toRad = function() {
      return this * Math.PI / 180;
   }
}

// Window.console override for older browsers
if(!window.console)
{
   var __console = function(){
      this.history = [];
   }
   __console.prototype.log = function()
   {
      this.history.push(Array.prototype.slice.call( arguments ));
   }
   window.console = new __console();
}

// Setup getCookie function if not exists
if(typeof getCookie != 'function')
{
   function getCookie(name) 
   {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') 
      {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) 
         {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) 
            {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
            }
         }
      }
      return cookieValue;
   }
}

// Adding indexOf method for searching arrays
if (!Array.prototype.indexOf)
{
  Array.prototype.indexOf = function(elt /*, from*/)
  {
    var len = this.length;

    var from = Number(arguments[1]) || 0;
    from = (from < 0)
         ? Math.ceil(from)
         : Math.floor(from);
    if (from < 0)
      from += len;

    for (; from < len; from++)
    {
      if (from in this &&
          this[from] === elt)
        return from;
    }
    return -1;
  };
}

// Get query string parameters
function getParameterByName(name)
{
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

///////////////////////////////////////
// The main Mutuality object
///////////////////////////////////////
var Mutuality = (function($){
   
   // The default dataType for jQuery AJAX calls
   $.ajaxSetup({  dataType: 'json' });
   
   var module = 
   {
      basePath : '',
      cache: { current: ["", ""], profile: {}, friends: {}, leftSlotLocked: false, rightSlotLocked: false },
      mpcache: { current: "", fofList: {}, favoritesList: {}, currentLoc: 0, profileCacheData: {} },
      history : [],
      token : null,
      init: function( token, basePath, success )
      {
         var self = this;
         this.token = token;
         this.basePath = basePath || this.basePath;
         this.loadProfile( this.token , function( profile ){
            self.cache.profile = profile;  
            if(success instanceof Function) success.call( self );
         });
         
         $(window).unload(function(){
            self = null;
         });
      },
      /* Private methods for making various requests */
      __post: function(url, params, onSuccess, onError)
      {
         this.__makeRequest('POST', url, params, onSuccess, onError);
      },
      __get: function(url, params, onSuccess, onError)
      {
         this.__makeRequest('GET', url, params, onSuccess, onError);
      },
      __put: function(url, params, onSuccess, onError)
      {
         var self = this;
         this.__makeRequest('PUT', url, params, onSuccess, onError, function(xhr, settings){
            self.__beforeSend(xhr, settings);
            xhr.setRequestHeader('X-HTTP-Method-Override', 'PUT');
         });
      },
      __beforeSend: function(xhr, settings) 
      {
         if (!(/^http(s)?:.*/.test(settings.url))) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            xhr.setRequestHeader('X-Requested-With', 'XML-Http-Request');
            xhr.setRequestHeader('Accept', 'application/json');
         }
      },
      __onError: function(xhr, err, msg)
      {
         console.log("Oops, something went wrong:\n\n"+msg);
      },
      __makeRequest:function(type, url, params, onSuccess, onError, beforeSend)
      {
         var self = this;
         
         $.ajax({
            beforeSend : beforeSend || this.__beforeSend,
            url        : self.basePath + url,
            type       : type || 'GET',
            data       : params || {},
            success    : onSuccess,
            error      : onError || this.__onError
         });
      },
      /* End of private methods */
      // Get current user profile by token
      // TODO: Security - make sure other user profile cannot be loaded
      loadProfile: function( token, success )
      {
         if(!this.token) return;
         var self = this;
         var url = 'api/getProfile/';
         
         this.__post(url, {token: this.token}, function(response){
            
            if(response.hasOwnProperty('facebookID'))
            {
               Mutuality.cache.profile = response;
               if(success instanceof Function) success.call(self, response);
            }
            else if (response.hasOwnProperty('notice'))
            {
               alert(response.notice);
            }             
         });
      },
      // Check to see if user profile is loaded
      profileLoaded: function()
      {
         return this.cache.profile.hasOwnProperty('facebookID') ? true : false;
      },
      // Get the img url for the profile picture of a given width/height for a particular facebook ID
      getProfilePictureURL: function(facebookID, width, height){
          if (!width || !height){
            return "https://graph.facebook.com/"  + facebookID + "/picture";
          }
          else{
            return "https://graph.facebook.com/"  + facebookID + "/picture?width=" + width + "&height=" + height;
          }
      },
      // Get the facebook url for a particular facebook ID
      getFacebookPageURL: function(facebookID){
        return "window.open('http://facebook.com/" + facebookID +"'); return false;";
      },
      // Get the JS to pop open a fb message dialog
      getSendNudgeURL: function(facebookID, userID, name, link, redirect){
        var sendJS = "FB.ui({ method: 'send', name: '" + name +"', link:'" + link + "', to:'" + userID + "'});"
        return sendJS;       
      },
      // Get the list of facebook friends for the current user
      loadFriendsList: function( success )
      {
         if(!this.token) return;
         var self = this;
         var url = 'api/getFriendList/';

         this.__post(url, {token: this.token}, function(response){

            Mutuality.cache.friends = response;
            if(success instanceof Function) success.call(self, response);

            if (response.hasOwnProperty('notice'))
            {
               alert(response.notice);
            }
         });         
      },
      // Get the rest of the information about a friend from his/her facebookID
      getFriendProfile: function ( facebookID ){
          for (i = 0; i<Mutuality.cache.friends.length;i++){
              if (Mutuality.cache.friends[i].facebookID == facebookID){
                  return Mutuality.cache.friends[i];
              }
          }
      },      
      // Get the rest of the information about a friendoffriend from his/her facebookID
      getFriendOfFriendProfile: function ( facebookID ){
          for (i = 0; i<Mutuality.mpcache.fofList.length;i++){
              if (Mutuality.mpcache.fofList[i].facebookID == facebookID){
                  return Mutuality.mpcache.fofList[i];
              }
          }
      },
      // Update users friend list in the mutuality backend
      updateFriendList: function ( number, success )
      {
          var self = this;
          this.__post('api/updateFriendList/', {token: this.token, numFriends: number }, function(response){
              if (response == true){
                  if(success instanceof Function) success.call(self);
              }
          });
      },      
      // See if Update friend list has been called before
      updateFriendListCalled: function ( success )
      {
          var self = this;
          this.__post('api/updateFriendListCalled/', {token: this.token }, function(response){
                  if(success instanceof Function) success.call(self);
          });
      },
      // Load a new match for the current user
      loadNewMatch: function ( leftSlotGender, rightSlotGender, leftLock, rightLock, success )
      {
          if (!this.token || !leftSlotGender || !rightSlotGender) return;

          var self = this;
          this.__post('api/getNewMatch/', {token: this.token, leftSlotGender: leftSlotGender, rightSlotGender: rightSlotGender, leftSlotLocked: leftLock, rightSlotLocked: rightLock, leftSlotID: this.cache.current[0], rightSlotID: this.cache.current[1]}, function(response){
          if (response.length == 2){
              if(success instanceof Function) success.call( self, response );
          }
          else{
              alert("Error: Couldn't load a new match.");
          }
        });
      },
      // Lock/unlock the left slot
      lockLeft: function(){
        this.cache.leftSlotLocked = !this.cache.leftSlotLocked;
      },
      // Lock/unlock the right slot
      lockRight: function(){
        this.cache.rightSlotLocked = !this.cache.rightSlotLocked;
      },
      // Submit a thumbs up rating
      rateMatchThumbsUp: function ( success ) {
        var self = this;
        self.__post('api/rateThumbsUp/', { token: this.token, leftSlotFacebookID: this.cache.current[0], rightSlotFacebookID: this.cache.current[1] } , function (response){
            if (response == true){
                if(success instanceof Function) success.call(self);
            }
            /*else
            {
                alert("Error: Couldn't rate thumbs up.");
            }*/
         });

      },
      // Submit a thumbs down rating
      rateMatchThumbsDown: function( reasons, success )
      {
        var self = this;
        
        self.__post('api/rateThumbsDown/', { token: this.token, leftSlotFacebookID: this.cache.current[0], rightSlotFacebookID: this.cache.current[1], reasons: reasons, numReasons: reasons.length}, function( response ){
           if(response == true)
           {
              if(success instanceof Function) success.call(self, response.profiles);
           }
           /*else
           {
              alert("Error: Couldn't rate thumbs down.");
           }*/
        });
      },
      // Get friends of friend
      getFriendsOfFriends: function( success )
      {
           var self = this;

           self.__post('api/getFriendsOfFriendsList/', { token: this.token }, function( response ){
               if(response.length > 1)
               {
                   if(success instanceof Function) success.call(self, response);
               }
               /*else
               {
                   alert("Error: No friends of friends found.");
               }*/
           });
       },
      // Get meet people list (fresh users, friendship)
      getMeetPeople: function(v, d, success )
      {
           var self = this;

           self.__post('api/getMeetPeople/', { token: this.token, viewed: v, dating: d }, function( response ){
               if(response)
               {
                   if(success instanceof Function) success.call(self, response);
               }
               /*else
               {
                   alert("Error: Meet people cannot be loaded.  No results.");
               }*/
           });
       }, 
      // Get meet people profile
      getMeetPeopleProfile: function( fbID, success )
      {
           var self = this;

           self.__post('api/getMeetPeopleProfile/', { facebookID: fbID }, function( response ){
               if('gender' in response)
               {
                   if(success instanceof Function) success.call(self, response);
               }
               /*else
               {
                   alert("Error: Meet people profile cannot be loaded.");
               }*/
           });
       },
    // Get your mutual friends with a particular person
    getMutualFriendList: function( fbID, success )
    {
         var self = this;

         self.__post('api/getMutualFriendList/', { token: this.token, facebookID: fbID }, function( response ){
             if(response.length > 0)
             {
                 if(success instanceof Function) success.call(self, response);
             }
             /*else
             {
                 alert("Error: No Mutual Friends.");
             }*/
         });
     },
     // Set a favorite
    setFavorite: function( fbID, success )
    {
         var self = this;

         self.__post('api/setFavorite/', { token: this.token, facebookID: fbID }, function( response ){
             if(response == true)
             {
                 if(success instanceof Function) success.call(self, response);
             }
             /*else
             {
                 alert("Error: Failed to add to favorites.");
             }*/
         });
     },     
    // Remove a favorite
    removeFavorite: function( fbID, success )
    {
         var self = this;

         self.__post('api/removeFavorite/', { token: this.token, facebookID: fbID }, function( response ){
             if(response == true)
             {
                 if(success instanceof Function) success.call(self, response);
             }
             /*else
             {
                 alert("Error: Failed to remove from favorites.");
             }*/
         });
     },
     // Get your favorites list
    getFavoritesList: function( success )
    {
         var self = this;

         self.__post('api/getFavoritesList/', { token: this.token }, function( response ){
             if(response.length > 0)
             {
                 if(success instanceof Function) success.call(self, response);
             }
             /*else
             {
                 alert("Error: No Favorites Added.");
             }*/
         });
     },
    // Set a user as viewed
    setUserViewed: function( fbID, success )
    {
         var self = this;

         self.__post('api/setUserViewed/', { token: this.token, facebookID: fbID }, function( response ){
             if(response)
             {
                 if(success instanceof Function) success.call(self, response);
             }
             else
             {
                 alert("Error: Failed to set user as viewed.");
             }
         });
     },
     // Get thread previews for messages
    getThreadPreviews: function( success )
    {
         var self = this;

         self.__post('api/getThreadPreviews/', { token: this.token }, function( response ){
             if(response)
             {
                 if(success instanceof Function) success.call(self, response);
             }
             else
             {
                 alert("Error: Failed get inbox threads.");
             }
         });
     },
     // Get messages with another facebook user
    getMessagesWithOther: function( fbID, success )
    {
         var self = this;

         self.__post('api/getMessagesWithOther/', { token: this.token, facebookID: fbID }, function( response ){
             if(response)
             {
                 if(success instanceof Function) success.call(self, response);
             }
             else
             {
                 alert("Error: Failed get messages with another user.");
             }
         });
     },
    // Get new message count
    getNewMessageCount: function( success )
    {
         var self = this;

         self.__post('api/getNewMessageCount/', { token: this.token }, function( response ){
             if(success instanceof Function) success.call(self, response); 
         });
     },
   // Send new message
    sendMessage: function(fbID, messageString, success )
    {
         var self = this;

         self.__post('api/sendMessage/', { token: this.token, otherFbId: fbID, messageContent: messageString }, function( response ){
             if(success instanceof Function) success.call(self, response); 
         });
     },
    // Set attributes of user profile
    setProfile: function( loc, relationship, gen, success )
    {
         var self = this;

         self.__post('api/setProfile/', { token: this.token, location: loc, relationship_status: relationship, gender: gen }, function( response ){
             if(success instanceof Function) success.call(self, response); 
         });
     }

 };
   return module;
})(jQuery);


