from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from la_facebook.models import UserAssociation
from connect.models import Profile
from django.views.decorators.csrf import csrf_protect

def index(request):
    context_dict = {}
    context_dict['request'] = request
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        print 
        try:
            if request.user.is_authenticated():
                profile = request.user.get_profile()
                context_dict['profile'] = profile
        except Profile.DoesNotExist:
            pass
    return render_to_response('index.html', context_dict, context_instance=RequestContext(request))

@login_required
def register(request):
    context_dict = {}
    context_dict['request'] = request
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID;
    context_dict['URL'] = settings.URL;
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        print
        try:
            if request.user.is_authenticated():
                profile = request.user.get_profile()
                context_dict['profile'] = profile
        except Profile.DoesNotExist:
            pass
    return render_to_response('register.html', context_dict, context_instance=RequestContext(request))

@login_required
def makematches(request):
    context_dict = {}
    context_dict['info'] = fbinfo(request)
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            profile = request.user.get_profile()
            context_dict['profile'] = profile
        except Profile.DoesNotExist:
            pass
        html = render_to_string('make-matches.html', RequestContext(request, context_dict))
        return HttpResponse(html)

@login_required
def meetpeople(request):
    context_dict = {}
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['info'] = fbinfo(request)
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            profile = request.user.get_profile()
            context_dict['profile'] = profile
        except Profile.DoesNotExist:
            pass
        html = render_to_string('meet-people.html', RequestContext(request, context_dict))
        return HttpResponse(html)

@login_required
def messages(request):
    context_dict = {}
    context_dict['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
    context_dict['info'] = fbinfo(request)
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            profile = request.user.get_profile()
            context_dict['profile'] = profile
        except Profile.DoesNotExist:
            pass
        html = render_to_string('messages.html', RequestContext(request, context_dict))
        return HttpResponse(html)


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