from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView

from connect.functions.setBeacon import SetBeacon

class SetBeaconAPI(APIView):
    """
    Set a user's beacon.
    """
    def get_object(self, pk, place, category):
        try:
            profile = Profile.objects.get(facebookID=pk)
            hasBeaconSet = SetBeacon(profile, place, category)
            #print hasBeaconSet
            return hasBeaconSet
        except Profile.DoesNotExist:
            raise Http404
        except:
            return False

    def post(self, request, format=None):
        hasBeaconSet = self.get_object(request.DATA['token'], request.DATA['place'], request.DATA['category'])
        print hasBeaconSet
        return hasBeaconSet
