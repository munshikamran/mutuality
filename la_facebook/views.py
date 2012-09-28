from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from la_facebook.access import OAuthAccess
from la_facebook.exceptions import MissingToken
from la_facebook.la_fb_logging import logger

import base64, hmac, hashlib
import simplejson as json
from django.conf import settings
from la_facebook.models import UserAssociation
from Mutuality.connect.models import Profile

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request, secret):
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        # log.error('Unknown algorithm')
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        # log.debug('valid signed request received..')
        return data

def facebook_login(request, redirect_field_name="next",
                        redirect_to_session_key="redirect_to",
                        display="page"):
    """
        1. access OAuth
        2. set token to none
        3. store and redirect to authorization url
        4. redirect to OAuth authorization url
    """
    
    access = OAuthAccess()
    token = None
    if hasattr(request, "session"):
        logger.debug("la_facebook.views.facebook_login: request has session")
        # this session variable is used by the callback
        request.session[redirect_to_session_key] = request.GET.get(redirect_field_name)
    if request.method == "POST":
        print "HELLO"
        data = parse_signed_request(request.POST['signed_request'], settings.FACEBOOK_APP_SECRET)
        print request.POST['signed_request']
        facebookid = data['user_id']
        user_id = UserAssociation.objects.get(identifier=facebookid).user_id
        profile = Profile.objects.get(user_id=user_id)
        print data['registration']['single']
        profile.single = bool(data['registration']['single'])
        print data
        print user_id
        print profile

    return HttpResponseRedirect(access.authorization_url(token, display=display))


def facebook_callback(request, error_template_name="la_facebook/fb_error.html"):
    """
        1. define RequestContext
        2. access OAuth
        3. check session
        4. autheticate token
        5. raise exception if missing token
        6. return access callback
        7. raise exception if mismatch token
        8. render error 
    """
    
    ctx = RequestContext(request)
    access = OAuthAccess()
    # TODO: Check to make sure the session cookie is setting correctly
    unauth_token = request.session.get("unauth_token", None)
    try:
        auth_token = access.check_token(unauth_token, request.GET)
    except MissingToken:
        ctx.update({"error": "token_missing"})
        logger.error('la_facebook.views.facebook_callback: missing token')
    else:
        if auth_token:
            logger.debug('la_facebook.views.facebook_callback: token success '\
                    ', sending to callback')
            return access.callback(request, access, auth_token)
        else:
            # @@@ not nice for OAuth 2
            ctx.update({"error": "token_mismatch"})
            logger.error('la_facebook.views.facebook_callback: token mismatch'\
                    ', error getting token, or user denied FB login')

    # we either have a missing token or a token mismatch
    # Facebook provides some error details in the callback URL
    fb_errors = []
    for fb_error_detail in ['error', 'error_description', 'error_reason']:
        if fb_error_detail in request.GET:
            ctx['fb_' + fb_error_detail] = request.GET[fb_error_detail]
            fb_errors.append(request.GET[fb_error_detail])

    logger.warning('la_facebook.views.facebook_callback: %s'
            % ', '.join(fb_errors))

    # Can't change to 401 error because that prompts basic browser auth
    return render_to_response(error_template_name, ctx)

'''
# TODO - delete or actually use.
# Probably unnecessary
def finish_signup(request):
    """
        1. access OAuth
        2. return callback url and finish signup
    """
    
    access = OAuthAccess()
    return access.callback.finish_signup(request)
'''
