from la_facebook.la_fb_logging import logger
from la_facebook.access import OAuthAccess
from la_facebook.access import OAuth20Token
from rest_framework.views import APIView
from rest_framework.response import Response
import django.utils.simplejson as json
import urllib
import cgi
from la_facebook.callbacks.default import DefaultFacebookCallback
from django.contrib.auth.models import User

class MobileAuthAPI(APIView):

    def post(self, request, format=None):
        
        #return 200 if user is already authenticated
        if request.user is not None :
            logger.debug("mobileauth invoked with user %s on session" % request.user);
            if request.user.is_authenticated():
                logger.debug("mobileauth invoked with authenticated user on session");
                return Response(user.id,status=200);

        #validate the access token by hitting graph.facebook.com
        fbAuthToken = request.DATA['access_token'];
        if fbAuthToken is None:
            return Response("access_token is missing", status=400);
        urlStream = urllib.urlopen("https://graph.facebook.com/me?access_token=%s" % fbAuthToken);
        raw_data = urlStream.read();
        fbResponseCode = urlStream.getcode();
        if fbResponseCode <> 200:
            logger.debug("failed to verify access token. response code: %s. message: %s" % (fbResponseCode, raw_data));
            return Response("failed to verify access token", status=500);
        response = json.loads(raw_data);
        fbUserId = response['id'];
        
        #let an instance of the LaFacebook default callback handle Django auth
        lafbCallback = DefaultFacebookCallback()
        existing_user = lafbCallback.lookup_user(None, None, response);
        logger.debug("existing user? %s" % existing_user);
        if existing_user is None:
            #create user record
            access = OAuthAccess()
            existing_user = lafbCallback.create_user(request._request, access, OAuth20Token(fbAuthToken), response);
        else:
            username = existing_user.username;
            logger.debug("query for user %s" % username);
            userObj = User.objects.get(username=username);
            lafbCallback.login_user(request._request, userObj);
            
        #return success & the user id if everything worked
        if existing_user.is_authenticated():
            return Response(fbUserId, status=200);
        else:
            return Response("Authentication failed for %s" % fbUserId, status=500);
