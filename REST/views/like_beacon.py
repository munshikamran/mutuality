from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.functions.likeBeacon import LikeBeacon

class LikeBeaconAPI(APIView):
    """
    Like a particular beacon.
    """
    def get_object(self, fbID):
        try:
            profile = Profile.objects.get(facebookID=fbID)
            hasBeaconLiked = LikeBeacon(profile, fbID)
            return hasBeaconLiked
        except Profile.DoesNotExist:
            raise Http404
        except:
            return False

    def post(self, request, format=None):
        hasBeaconLiked = self.get_object(request.DATA['fbID'])
        return Response(hasBeaconLiked)
