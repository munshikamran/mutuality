from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.setBeacon import SetBeacon

class SetBeaconAPI(APIView):
    """
    Set a user's beacon.
    """
    def get_object(self, fbID, place, activity, category):
        try:
            profile = Profile.objects.get(facebookID=fbID)
            hasBeaconSet = SetBeacon(profile, place, activity, **{"categoryName":category})
            return hasBeaconSet
        except Profile.DoesNotExist:
            raise Http404
        except:
            return False

    def post(self, request, format=None):
        hasBeaconSet = self.get_object(request.DATA['token'], request.DATA['place'], request.DATA['activity'], request.DATA['categoryName'])
        return Response(hasBeaconSet)
