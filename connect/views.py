from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from la_facebook.models import UserAssociation
from connect.models import Profile
from django.shortcuts import redirect
from connect.functions.updateFriendList import UpdateFriendListHasBeenCalled
from connect.functions.viewPage import PageHasBeenViewed, ViewPage
from common.enums.site_pages import SITE_PAGES
from datetime import datetime
from connect.functions.getProfileAuthToken import GetProfileAuthToken
from connect.functions.getBeacon import GetBeacon
from connect.models.pageView import PageView
from rest_framework.authtoken.models import Token
from datetime import datetime
from datetime import timedelta
import facebook

def index(request):
    context_dict = {}
    context_dict['request'] = request
    context_dict['URL'] = settings.URL
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            if request.user.is_authenticated():
                profile = request.user.get_profile()
                authtoken = Token.objects.get(user=request.user).key
                context_dict['rest_token'] = authtoken
                context_dict['profile'] = profile
                return HttpResponseRedirect("/meetpeople/")
        except Profile.DoesNotExist:
            pass
    return render_to_response('index.html', context_dict, context_instance=RequestContext(request))

@login_required
def register(request):
    context_dict = {}
    context_dict['request'] = request
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['URL'] = settings.URL
    noProfile = False
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            if request.user.is_authenticated():
                #Get the profile
                profile = request.user.get_profile()
                authtoken = Token.objects.get(user=request.user).key
                context_dict['rest_token'] = authtoken
                context_dict['profile'] = profile

                #Get the birthday
                if profile.birthdayString:
                    bdayStringArr = profile.birthdayString.split("'")
                    if len(bdayStringArr) > 5:
                        context_dict['birthday'] = bdayStringArr[1] + "-" + bdayStringArr[3] + "-" + bdayStringArr[5]

                #Get other fields using graph api to populate more inputs if necessary
                #graph = facebook.GraphAPI(GetProfileAuthToken(profile))
                #print GetProfileAuthToken(profile)
                #fields = ["location"]
                #kwargs = {"fields": fields}
                #data=graph.get_object(profile.facebookID,**kwargs)
                #locationData = graph.get_object(data['location']['id'])
        except Profile.DoesNotExist:
            noProfile = True
            pass
    if (noProfile or UpdateFriendListHasBeenCalled(profile)):
        return redirect("/meetpeople/")
    else:
        return render_to_response('register.html', context_dict, context_instance=RequestContext(request))

@login_required
def account(request):
    context_dict = {}
    context_dict['request'] = request
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['URL'] = settings.URL
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            if request.user.is_authenticated():
                #Get the profile and the auth_token
                profile = request.user.get_profile()
                ViewPage(profile, SITE_PAGES.ACCOUNT)
                authtoken = Token.objects.get(user=request.user).key
                context_dict['rest_token'] = authtoken
                context_dict['profile'] = profile
                context_dict['AUTH_TOKEN'] = GetProfileAuthToken(profile)
                #Get location lat/long to pass to template so that places dropdown results are narrowed
                graph = facebook.GraphAPI(GetProfileAuthToken(profile))
                fields = ["location"]
                kwargs = {"fields": fields}
                data=graph.get_object(profile.facebookID,**kwargs)
                locationData = graph.get_object(data['location']['id'])
                context_dict['LAT'] = locationData['location']['latitude']
                context_dict['LONG'] = locationData['location']['longitude']
        except Profile.DoesNotExist:
            pass
    return render_to_response('account.html', context_dict, context_instance=RequestContext(request))

@login_required
def beacon(request):
    context_dict = {}
    context_dict['request'] = request
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['URL'] = settings.URL
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            if request.user.is_authenticated():
                #Get the profile and the auth_token
                profile = request.user.get_profile()
                ViewPage(profile, SITE_PAGES.BEACON)
                authtoken = Token.objects.get(user=request.user).key
                context_dict['rest_token'] = authtoken
                context_dict['profile'] = profile
                context_dict['AUTH_TOKEN'] = GetProfileAuthToken(profile)
                #Get the beacon for this user account page
                beacon = GetBeacon(profile)
                if beacon != []:
                    context_dict['beacon'] = GetBeacon(profile)

                #Get location lat/long to pass to template so that places dropdown results are narrowed
                graph = facebook.GraphAPI(GetProfileAuthToken(profile))
                if profile.location:
                    fields = ["location"]
                    kwargs = {"fields": fields, "q": profile.location, "type": "place"}
                    data = graph.get_object("search", **kwargs)
                    if len(data) > 0:
                        context_dict['LAT'] = data['data'][0]['location']['latitude']
                        context_dict['LONG'] = data['data'][0]['location']['longitude']
                else:
                    # if for whatever reason they do not have a location set, default to seattle lat/long
                    context_dict['LAT'] = 47.6097
                    context_dict['LONG'] = 122.3331
        except Profile.DoesNotExist:
            pass
    return render_to_response('beacon.html', context_dict, context_instance=RequestContext(request))

@login_required
def makematches(request):
    context_dict = {}
    context_dict['info'] = fbinfo(request)
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['URL'] = settings.URL
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            profile = request.user.get_profile()
            authtoken = Token.objects.get(user=request.user).key
            context_dict['rest_token'] = authtoken
            context_dict['profile'] = profile
            ViewPage(profile, SITE_PAGES.MAKE_MATCHES)
        except Profile.DoesNotExist:
            pass
        html = render_to_string('make-matches.html', RequestContext(request, context_dict))
        return HttpResponse(html)

@login_required
def meetpeople(request):
    context_dict = {}
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['info'] = fbinfo(request)
    context_dict['URL'] = settings.URL
    request.session.set_expiry(604800)  # one week
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        request.session['last_login_date'] = datetime.now()
        request.user.last_login = datetime.now()
        request.user.save()
        try:
            profile = request.user.get_profile()
            authtoken = Token.objects.get(user=request.user).key
            context_dict['rest_token'] = authtoken
            context_dict['profile'] = profile

            #if user has not seen/gone to invite page for 5 days, redirect them
            pageView = None
            try:
                pageView = PageView.objects.filter(user=profile, page_viewed=SITE_PAGES.INVITE).latest('date_viewed')
            except PageView.DoesNotExist:
                return redirect("/share/")

            if pageView is not None:
                fiveDaysAgo = datetime.now() - timedelta(5)
                if pageView.date_viewed.date() < fiveDaysAgo.date():
                    return redirect("/share/")
            ViewPage(profile, SITE_PAGES.MEET_PEOPLE)
        except Profile.DoesNotExist:
            pass
        html = render_to_string('meet-people.html', RequestContext(request, context_dict))
        return HttpResponse(html)

@login_required
def messages(request):
    context_dict = {}
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['info'] = fbinfo(request)
    context_dict['URL'] = settings.URL
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            profile = request.user.get_profile()
            authtoken = Token.objects.get(user=request.user).key
            context_dict['rest_token'] = authtoken
            context_dict['profile'] = profile
            if(PageHasBeenViewed(profile, SITE_PAGES.MESSAGES)):
                context_dict['viewed'] = True
            ViewPage(profile, SITE_PAGES.MESSAGES)
        except Profile.DoesNotExist:
            pass
        html = render_to_string('messages.html', RequestContext(request, context_dict))
        return HttpResponse(html)

@login_required
def share(request):
    context_dict = {}
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['info'] = fbinfo(request)
    context_dict['URL'] = settings.URL
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            profile = request.user.get_profile()
            authtoken = Token.objects.get(user=request.user).key
            context_dict['rest_token'] = authtoken
            context_dict['profile'] = profile
            ViewPage(profile, SITE_PAGES.INVITE)
        except Profile.DoesNotExist:
            pass
        html = render_to_string('share.html', RequestContext(request, context_dict))
        return HttpResponse(html)

def about(request):
    context_dict = {}
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['info'] = fbinfo(request)
    context_dict['URL'] = settings.URL
    return render_to_response('about.html', context_dict, context_instance=RequestContext(request))


def privacy(request):
    context_dict = {}
    return render_to_response('privacy.html', context_dict, context_instance=RequestContext(request)) 

def fbinfo(request):
    """ A view for returning a dict of info about FB and user status """
    info = {}
    if request.user.is_authenticated():
        info['User Authenticated'] = 'Yes'
        if request.user.has_usable_password():
            info['Authed via'] = 'Django'
            info['Django username'] = str(request.user)
        else:
            info['Authed via'] = "Facebook"
            try:
                assoc_obj = UserAssociation.objects.get(user=request.user)
            except UserAssociation.DoesNotExist:
                info['Association Object'] = "not found"
            else:
                info['Associated FB Token Expires'] = assoc_obj.expires
                info['Facebook ID'] = assoc_obj.identifier
    else:
        info['User Authenticated'] = 'No'
    info['Session Expires'] = request.session.get_expiry_date()
    try:
        info['Facebook App ID'] = settings.FACEBOOK_ACCESS_SETTINGS["FACEBOOK_APP_ID"]
    except (KeyError, AttributeError):
        info['Facebook App ID'] = "Not Configured"
    context_dict = {}
    context_dict['info'] = sorted(info.items())
    return render_to_response('fbinfo.html', context_dict, context_instance=RequestContext(request))
