from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.likeBeacon import GetBeaconLikeCount
from connect.functions.getBeacon import GetBeacon

class GetBeaconLikeCountAPI(APIView):
    """
    Get a user's beacon like count.
    """
    def get_object(self, fbID):
        try:
            profile = Profile.objects.get(facebookID=fbID)
            beacon = GetBeacon(profile)
            likeCount = GetBeaconLikeCount(beacon)
            return likeCount
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        likeCount = self.get_object(request.DATA['fbID'])
        return Response(likeCount)