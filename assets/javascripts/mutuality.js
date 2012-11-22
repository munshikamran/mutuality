//
//  mutuality.js
//  Mutuality Main Library
//  
//  Created by Craig Hoover obo Lee Peterson
//  Copyright 2012 Mutuality LLC. All rights reserved.
// 

   ///////////////////////////////////////
 // Utility functions and preloads
//


// add method to number for rad lookup
if (typeof(Number.prototype.toRad) === "undefined") {
   Number.prototype.toRad = function() {
      return this * Math.PI / 180;
   }
}

// window.console override for older browsers
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

// setup getCookie function if not exists
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

// indexOf method for searching arrays
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
 // Main object
//
var Mutuality = (function($){
   
   // default dataType for jQuery Ajax calls
   $.ajaxSetup({  dataType: 'json' });
   
   var module = 
   {
      basePath : '',
      cache: { current: [], profile: {}, friends: {}, matches: {}, locked: [] },
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
      // private "style" methods for making requests
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
      // get current user profile by token
      // obviously, the server side will need to make sure that
      // there is an ACL to make sure the current user can't load
      // the profile of another user - perhaps a comparison of the
      // session user token vs what is posted
      loadProfile: function( token, success )
      {
         if(!this.token) return;
         var self = this;
         var url = 'api/getProfile/';
         
         this.__post(url, {token: this.token}, function(response){
            
            if(response.hasOwnProperty('profile'))
            {
               // Mutuality.cache.profile = response.profile;    
               if(success instanceof Function) success.call(self, response.profile);
            }
            else if (response.hasOwnProperty('notice'))
            {
               alert(response.notice);
            }             
         });
      },
      // check to see if user profile is loaded
      profileLoaded: function()
      {
         return this.cache.profile.hasOwnProperty('token') ? true : false;
      },
      // get a list of friends for the current user
      loadFriendsList: function( gender , success )
      {
         if(!this.token) return;
         var self = this;
         
         // underscore used as you can't name a file and folder
         // the same name.  optimally the url should be:
         //  /friends/list/male(female)?token=[token]
         
         var gender = gender || null;         
         var url = 'api/getFriendList/';
         
         //
         // optimial RESTful URLs:
         //
         //  /[token]/friends/list - get all friends
         //  /[token]/friends/list/male
         //  /[token]/friends/list/female
         //
         // acceptable structure
         //
         //  /friends/list?token=[token]
         //  /friends/list/male?token=[token]
         //  /friends/list/female?token=[token]
         //
         this.__post(url, {token: this.token}, function(response){
            
            if(response.hasOwnProperty('profiles'))
            {
               // Mutuality.cache.friends = response.profiles;               
               if(success instanceof Function) success.call(self, response.profiles);   
 
            }
            else if (response.hasOwnProperty('notice'))
            {
               alert(response.notice);
            }
         });         
      },
      loadFriendMatches: function( token, gender , success)
      {
         if( !token || !gender ) return;
         var self = this;
         
         // make request to find friend matches by selected token
         //
         //  /friends/matches/female?token=[token]
         //  /friends/matches/male?token=[token]         
         //
         this.__post('friends/matches/'+gender, {token: token}, function(response){

            if(response.hasOwnProperty('profiles'))
            {
               // cache our results by token
               // Mutuality.cache.matches[selected] = response.profiles;
               if(success instanceof Function) success.call( self, response.profiles );
            }
            else if (response.hasOwnProperty('notice'))
            {
               alert(response.notice);
            }      
         });
      },
      // get local cached friend profile by token and (optional) gender
      getFriendProfile : function( token, gender )
      {
         var self = this;
         var found = null;
         var genders = gender ? [gender] : ['male','female'];

         for(var i=0, len = genders.length;i<len;i++){
         
            var gender = genders[i];
         
            if(self.cache.friends.hasOwnProperty(gender))
            {
               var list = self.cache.friends[gender];
               
               for(var j = 0, len = list.length; j<len; j++)
               {
                  if(token === list[j].token)
                  {
                     found = list[j];
                     break;
                  }
               }
            }
         }   
         return found;      
      },
      // rate a friend. reason is an ID of reasons
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
      },
      // add token for locked friend to locked array
      lockFriend: function( token )
      {
         var found = this.cache.locked.indexOf( token ); 
         if(found == -1)
         {
            this.cache.locked.push( token );
         }
      },
      // remove token for locked friend from locked array
      unlockFriend: function( token )
      {
         var found =  this.cache.locked.indexOf( token );
         if(found > -1)
         {
            delete(this.cache.locked[ found ]);
         }
      },
      // test if friend is locked
      friendLocked: function( token )
      {
         return this.cache.locked.indexOf( token ) > -1  ? true : false;
      }       
   };
   return module;
})(jQuery);


