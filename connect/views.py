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

def index(request):
    context_dict = {}
    context_dict['request'] = request
    context_dict['URL'] = settings.URL
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        print 
        try:
            if request.user.is_authenticated():
                profile = request.user.get_profile()
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
        print
        try:
            if request.user.is_authenticated():
                profile = request.user.get_profile()
                context_dict['profile'] = profile
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
        print
        try:
            if request.user.is_authenticated():
                profile = request.user.get_profile()
                context_dict['profile'] = profile
        except Profile.DoesNotExist:
            pass
    return render_to_response('account.html', context_dict, context_instance=RequestContext(request))


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
            context_dict['profile'] = profile
            if(PageHasBeenViewed(profile, SITE_PAGES.MAKE_MATCHES )):
                context_dict['viewed'] = True
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
    request.session.set_expiry(604800) # one week
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        if "last_login_date" in request.session.keys():
            if (request.session['last_login_date'].date() != datetime.now().date()):
                print "Updating last login!"
                request.session['last_login_date'] = datetime.now()
                request.user.last_login = datetime.now()
        else:
            request.session['last_login_date'] = datetime.now()
            request.user.last_login = datetime.now()
        try:
            profile = request.user.get_profile()
            context_dict['profile'] = profile
            if(PageHasBeenViewed(profile, SITE_PAGES.MEET_PEOPLE )):
                context_dict['viewed'] = True
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
            context_dict['profile'] = profile
            if(PageHasBeenViewed(profile, SITE_PAGES.MESSAGES )):
                context_dict['viewed'] = True
            ViewPage(profile, SITE_PAGES.MESSAGES)
        except Profile.DoesNotExist:
            pass
        html = render_to_string('messages.html', RequestContext(request, context_dict))
        return HttpResponse(html)

def about(request):
    info = {}
    #context_dict['URL'] = settings.URL
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
    return render_to_response('about.html', context_dict, context_instance=RequestContext(request))

def faq(request):
    info = {}
    #context_dict['URL'] = settings.URL
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
    return render_to_response('faq.html', context_dict, context_instance=RequestContext(request)) 

def privacy(request):
    info = {}
    #context_dict['URL'] = settings.URL
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