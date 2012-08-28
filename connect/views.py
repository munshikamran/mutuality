from django.conf import settings
from django.shortcuts import render_to_response
from Mutuality.connect.models import Profile
from django.contrib.auth.decorators import login_required

from la_facebook.models import UserAssociation

def fbinfo(request):
    """ returns a dict of info about FB and user status """
    info = {}
    if request.user.is_authenticated():
        info['User Authenticated'] = 'Yes'
        if request.user.has_usable_password():
            info['Authed via'] = 'Django'
            info['Django username'] = str(request.user)
        else:
            info['Authed via'] = "FaceBook"
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
    return render_to_response('fbinfo.html', context_dict) 

def index(request):
    context_dict = {}
    context_dict['request'] = request
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        print 
        try:
            if request.user.is_authenticated():
                context_dict['profile'] = request.user.get_profile()
        except Profile.DoesNotExist:
            pass
    return render_to_response('index.html', context_dict)

@login_required
def profile(request):
    # Let's prove facebook's creepy stalker-ware is working
    # TODO: Needs a lot of validation
    context_dict = {}
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            context_dict['profile'] = request.user.get_profile()
            context_dict['profile_pic'] = request.user.get_profile().imageURL()
        except Profile.DoesNotExist:
            pass
        
    
    return render_to_response('profile.html', context_dict)

@login_required
def dashboard(request):
    context_dict = {}
    context_dict['info'] = fbinfo(request)
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            context_dict['profile'] = request.user.get_profile()
            context_dict['profile_pic'] = request.user.get_profile().imageURL()
        except Profile.DoesNotExist:
            pass
        
    
    return render_to_response('dashboard.html', context_dict)
