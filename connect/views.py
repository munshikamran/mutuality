from django.conf import settings
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.contrib.auth.decorators import login_required

from Mutuality.connect.models import Profile
from slotMachine import SlotMachine
from la_facebook.models import UserAssociation

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
                context_dict['facebookID'] = profile.facebookID()
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
            context_dict['facebookID'] = profile.facebookID()
            slotMachine = SlotMachine(profile)
            request.session['slotMachine'] = slotMachine

        except Profile.DoesNotExist:
            pass
        html = render_to_string('make-matches.html', RequestContext(request, context_dict))
        return HttpResponse(html)

class LazyEncoder(simplejson.JSONEncoder):
    """Encodes django's lazy i18n strings.
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

def spinSlotMachine(request):
    if request.method == "POST":
        slotMachine = request.session['slotMachine']
        slotMachine.leftSlotLocked = "leftlocked" in request.POST.keys()
        slotMachine.rightSlotLocked = "rightlocked" in request.POST.keys();
        type = "success"
        slotMachine.spinButtonPressed()
        message = slotMachine.getStateString()
        leftslot=slotMachine.leftSlot
        rightslot=slotMachine.rightSlot
        request.session['slotMachine'] = slotMachine
    if request.is_ajax():
        result = simplejson.dumps({
            "leftslot": leftslot,
            "rightslot": rightslot,
            "message": message,
            "type": type,
        }, cls=LazyEncoder)
        return HttpResponse(result, mimetype='application/javascript')

def submitRating(request):
    if request.method == "POST":
        slotMachine = request.session['slotMachine']
        type = "success"
        if 'rating' in request.POST:
            rating = int(request.POST['rating'])
            slotMachine.setRating(rating)
            slotMachine.rateButtonPressed()
            message = "Rated: " + slotMachine.leftSlot['name'] + " and " + slotMachine.rightSlot['name']
        else:
            message = "Rating not posted."
        request.session['slotMachine'] = slotMachine
    if request.is_ajax():
        result = simplejson.dumps({
            "message": message,
            "type": type,
        }, cls=LazyEncoder)
        return HttpResponse(result, mimetype='application/javascript')

def friends_list(request):
  if request.is_ajax():
    message = {
       "profiles" : {
          "male" : [
             {
                "token" : "as8f9743kcyt9y3kctckcog5tmyBSDg",
                "full_name": "Brian Griffin",
                "dob": "1973-03-06",
                "relationship_status": "single",
                "city" : "Seattle",
                "state" : "WA",
                "image": "/assets/images/brian.jpg",
                "lat": 47.587877,
                "lng": -122.248457
             },
             {
                "token" : "l3Skf743kLD95J7Dj49Hsog5tmyBSDg",
                "full_name": "John Griffin",
                "dob": "1976-09-03",
                "relationship_status": "single",
                "city" : "Seattle",
                "state" : "WA",
                "image": "/assets/images/john.jpg",
                "lat": 47.587877,
                "lng": -122.248457
             }   
          ],
          "female" : [
             {
                "token" : "9sdfAvbWVRbt9jbgr9g35jb0qtjjb03b",
                "full_name" : "Betty Draper",
                "dob": "1976-10-16",
                "relationship_status": "single",
                "city" : "Lynnwood",
                "state" : "WA",
                "image" : "/assets/images/betty.jpg",
                "lat": 47.604541,
                "lng" : -122.547357
             },
             {
                "token" : "lSyJ94VRbt9jbgr9g35jb0qtjjb03b",
                "full_name" : "Susan Draper",
                "dob": "1978-08-02",
                "relationship_status": "single",
                "city" : "Lynnwood",
                "state" : "WA",
                "image" : "/assets/images/susan.jpg",
                "lat": 47.604541,
                "lng" : -122.547357
             }
          ]
       }
    }
  else:
    message = "Invalid request"
    
  json = simplejson.dumps(message)
  return HttpResponse(json, mimetype='application/json')

def friends_list_male(request):
    if request.is_ajax():
        message = {
           "profiles" : {
              "male" : [
                 {
                    "token" : "as8f9743kcyt9y3kctckcog5tmyBSDg",
                    "full_name": "Brian Griffin",
                    "dob": "1973-03-06",
                    "relationship_status": "single",
                    "city" : "Seattle",
                    "state" : "WA",
                    "image": "/assets/images/brian.jpg",
                    "lat": 47.587877,
                    "lng": -122.248457
                 },
                 {
                    "token" : "l3Skf743kLD95J7Dj49Hsog5tmyBSDg",
                    "full_name": "John Griffin",
                    "dob": "1976-09-03",
                    "relationship_status": "single",
                    "city" : "Seattle",
                    "state" : "WA",
                    "image": "/assets/images/john.jpg",
                    "lat": 47.587877,
                    "lng": -122.248457
                 }   
              ]
           }
        }
    else:
        message = "Invalid request"
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')

def friends_list_female(request):
    if request.is_ajax():
        message = {
           "profiles" : {
              "female" : [
                 {
                    "token" : "9sdfAvbWVRbt9jbgr9g35jb0qtjjb03b",
                    "full_name" : "Betty Draper",
                    "dob": "1976-10-16",
                    "relationship_status": "single",
                    "city" : "Lynnwood",
                    "state" : "WA",
                    "image" : "/assets/images/betty.jpg",
                    "lat": 47.604541,
                    "lng" : -122.547357
                 },
                 {
                    "token" : "lSyJ94VRbt9jbgr9g35jb0qtjjb03b",
                    "full_name" : "Susan Draper",
                    "dob": "1978-08-02",
                    "relationship_status": "single",
                    "city" : "Lynnwood",
                    "state" : "WA",
                    "image" : "/assets/images/susan.jpg",
                    "lat": 47.604541,
                    "lng" : -122.547357
                 }
              ]
           }
        }
    else:
        message = "Invalid request"
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')

def get_profile(request):
  if True:
    message =    { "profile" : {
      "token" : "vB8flDHD3IAS933kctckcog5tmyBSDg",
      "full_name": "Craig Hoover",
      "dob": "1975-03-06",
      "relationship_status": "married",
      "city" : "Gaithersburg",
      "state" : "MD",
      "image": "mutuality/html/images/craig.jpg",
      "lat": 47.587877,
      "lng": -122.248457
        }
    }
  else:
    message = "Invalid request"
    
  json = simplejson.dumps(message)
  return HttpResponse(json, mimetype='application/json')

