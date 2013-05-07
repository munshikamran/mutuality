from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from REST.serializers import BeaconResponseSerializer
from connect.functions.getBeacon import GetBeacon
from connect.functions.getBeaconLikes import GetBeaconLikes
from connect.classes.beaconResponse import BeaconResponse

class GetBeaconAPI(APIView):
    """
    Get a user's beacon.
    """
    def get_beacon(self, fbID):
        try:
            profile = Profile.objects.get(facebookID=fbID)
            beacon = GetBeacon(profile)
            return beacon
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        beacon = self.get_beacon(request.DATA['fbID'])
        beaconLikes = []
        if beacon != []:
            beaconLikes = GetBeaconLikes(beacon)
        beaconResponse = BeaconResponse(beacon, beaconLikes)
        serializer = BeaconResponseSerializer(beaconResponse)
        return Response(serializer.data)