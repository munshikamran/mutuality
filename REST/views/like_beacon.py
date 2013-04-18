from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from connect.functions.likeBeacon import LikeBeacon

class LikeBeaconAPI(APIView):
    """
    Like a particular beacon.
    """
    def get_object(self, fbID, facebookID):
        try:
            profile = Profile.objects.get(facebookID=fbID)
            hasBeaconLiked = LikeBeacon(profile, facebookID)
            return hasBeaconLiked
        except Profile.DoesNotExist:
            raise Http404
        except:
            return False

    def post(self, request, format=None):
        hasBeaconLiked = self.get_object(request.DATA['token'], request.DATA['facebookID'])
        return hasBeaconLiked
