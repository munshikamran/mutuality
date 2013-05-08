from la_facebook.la_fb_logging import logger
from la_facebook.access import OAuthAccess
from la_facebook.access import OAuth20Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from la_facebook.callbacks.default import DefaultFacebookCallback
from django.contrib.auth.models import User
from django.middleware import csrf
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
import facebook


class MobileAuthAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        print request.user
        #return 200 if user is already authenticated
        if request.user is not None:
            logger.debug("mobileauth invoked with user %s on session" % request.user)
            if request.user.is_authenticated():
                logger.debug("mobileauth invoked with authenticated user on session")
                return Response(None, status=204)

        #validate the access token by hitting graph.facebook.com
        fbAuthToken = request.DATA['access_token']
        if fbAuthToken is None:
            return Response("access_token is missing", status=400)
        graph = facebook.GraphAPI(fbAuthToken)
        try:
            graph_response = graph.get_object('me')
        except facebook.GraphAPIError as e:
            logger.warn(e)
            return Response("failed to verify access token", status=500)

        fbUserId = graph_response['id']
        #let an instance of the LaFacebook default callback handle Django auth
        lafbCallback = DefaultFacebookCallback()
        existing_user = lafbCallback.lookup_user(None, None, graph_response)
        logger.debug("existing user? %s" % existing_user)
        if existing_user is None:
            #create user record
            access = OAuthAccess()
            existing_user = lafbCallback.create_user(request._request, access, OAuth20Token(fbAuthToken),
                                                     graph_response)
        else:
            username = existing_user.username
            logger.debug("query for user %s" % username)
            userObj = User.objects.get(username=username)
            lafbCallback.login_user(request._request, userObj)

        #return success & the user id if everything worked
        response = {'id': graph_response['id']}
        logger.debug("existing_user %s", existing_user)
        response['token'] = Token.objects.get(user=existing_user).key
        logger.debug("csrf dict: %s" % csrf.get_token(request))
        if existing_user.is_authenticated():
            return Response(response, status=200)
        else:
            return Response("Authentication failed for %s" % fbUserId, status=500)

    #register a signal to create RestFramework auth tokens when
    #  new users are saved
    @receiver(post_save, sender=User)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        print "received user post-save signal"
        if created:
            Token.objects.create(user=instance)



