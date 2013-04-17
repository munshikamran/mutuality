from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from REST.serializers import BeaconSerializer

from connect.functions.getBeacon import GetBeacon

class GetBeaconAPI(APIView):
    """
    Get a user's beacon.
    """
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(facebookID=pk)
            beacon = GetBeacon(profile)
            return beacon
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        beacon = self.get_object(request.DATA['token'])
        serializer = BeaconSerializer(beacon)
        return Response(serializer.data)
