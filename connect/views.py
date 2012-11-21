from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from la_facebook.models import UserAssociation
from Mutuality.connect.models import Profile
# from Mutuality.slotMachine import SlotMachine
from django.utils.encoding import force_unicode
from django.utils.functional import Promise
import simplejson


def fbinfo(request):
    """ returns a dict of info about FB and user status """
    info = {}
    context_dict = {}
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
    print request
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        print 
        try:
            if request.user.is_authenticated():
                profile = request.user.get_profile()
                context_dict['profile'] = profile
                context_dict['facebookID'] = profile.facebookID
        except Profile.DoesNotExist:
            pass
    return render_to_response('index.html', context_dict)

def register(request):
    context_dict = {}
    context_dict['request'] = request
    return render_to_response('register.html', context_dict)

@login_required
def profile(request,facebookid):
    # Let's prove facebook's creepy stalker-ware is working
    # TODO: Needs a lot of validation
    context_dict = {}
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            user_id = UserAssociation.objects.get(identifier=facebookid).user_id
            profile = Profile.objects.get(user_id=user_id)
            context_dict['profile'] = profile
            context_dict['profile_pic'] = profile.imageURL()
            context_dict['facebookID'] = profile.facebookID()
            # context_dict['profile'] = request.user.get_profile()
            # context_dict['profile_pic'] = request.user.get_profile().imageURL()
        except Profile.DoesNotExist:
            pass
        
    
    return render_to_response('profile.html', context_dict)

@login_required
def makematches(request):
    context_dict = {}
    context_dict['info'] = fbinfo(request)
    if hasattr(request, 'user'):
        context_dict['user'] = request.user
        try:
            profile = request.user.get_profile()
            context_dict['profile'] = profile
            context_dict['profile_pic'] = profile.imageURL()
            context_dict['facebookID'] = profile.facebookID
            #slotMachine = SlotMachine(profile)
            #request.session['slotMachine'] = slotMachine

        except Profile.DoesNotExist:
            pass
        html = render_to_string('make-matches.html', RequestContext(request, context_dict))
        return HttpResponse(html)

