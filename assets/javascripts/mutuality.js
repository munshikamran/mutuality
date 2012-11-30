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
      // Private methods for making various requests
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
         alert("Oops, something went wrong:\n\n"+msg);
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
      getProfilePictureURL: function(facebookID){
          return "https://graph.facebook.com/"  + facebookID + "/picture?width=350&height=350"
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
      // Load a new match for the current user
      loadNewMatch: function ( leftSlotGender, rightSlotGender, success )
      {
          if (!this.token || !leftSlotGender || !rightSlotGender) return;
          var self = this;
          this.__post('api/getNewMatch/', {token: this.token, leftSlotGender: leftSlotGender, rightSlotGender: rightSlotGender, leftSlotLocked: this.cache.leftSlotLocked, rightSlotLocked: this.cache.rightSlotLocked, leftSlotID: this.cache.current[0], rightSlotID: this.cache.current[1]}, function(response){
            if(success instanceof Function) success.call( self, response );
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
      // Rate a match.
      // reason is an ID of reasons
      // if not specified or 0, rating is positive
      rateFriend: function( matchToken, rateToken, reason, success )
      {
        var self = this; 
        var reason = reason || 0;
        if( !matchToken || !rateToken ) return;
        
        self.__post('/friends/rate', { matchToken: matchToken, rateToken: rateToken, reason: reason}, function( response ){
           
           if(response.hasOwnProperty('profiles'))
           {
              // Mutuality.cache.matches[matchToken] = response.profiles;
              if(success instanceof Function) success.call(self, response.profiles);
           }
           else if (response.hasOwnProperty('notice'))
           {
              alert(response.notice);
           }
        });
      }
   };
   return module;
})(jQuery);

