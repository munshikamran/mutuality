from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from REST.serializers import BeaconSerializer

from connect.functions.getHasLikedBeacon import hasLikedBeacon

class GetHasLikedBeaconAPI(APIView):
    """
    Get a user's beacon.
    """
    def get_object(self, myFbID, theirFbID):
        try:
            myProfile = Profile.objects.get(facebookID=myFbID)
            HasLikedBeacon = hasLikedBeacon(myProfile, theirFbID)
            return HasLikedBeacon
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        HasLikedBeacon = self.get_object(request.DATA['token'], request.DATA['fbID'])
        return Response(HasLikedBeacon)