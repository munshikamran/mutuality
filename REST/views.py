from django.http import Http404
from django.http import HttpResponse
from django.utils import simplejson

from Mutuality.connect.models import Profile
from REST.serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProfileDetail(APIView):
    """
    Retrieve, update or delete a Profile.
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(facebookID=pk)
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def friends_list(request):
    if True:
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

