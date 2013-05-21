from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from REST.serializers import BeaconResponseSerializer
from connect.functions.getBeacon import GetBeacon
from connect.functions.getBeaconLikes import GetBeaconLikes
from connect.classes.beaconResponse import BeaconResponse
from connect.functions.getProfileAuthToken import GetProfileAuthToken
import facebook

class GetBeaconAPI(APIView):
    """
    Get a user's beacon.
    """
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['fbID'])
            beacon = GetBeacon(profile)
        except Profile.DoesNotExist:
            raise Http404

        beaconLikes = []
        if beacon != []:
            beaconLikes = GetBeaconLikes(beacon)

        graph = facebook.GraphAPI(GetProfileAuthToken(profile))
        fields = ['name', 'location']
        kwargs = {"type": "place", "q": str(beacon.place),  "fields": fields}
        data = graph.get_object("search", **kwargs)
        latitude = 0.0
        longitude = 0.0
        if len(data['data']) != 0:
            latitude = data['data'][0]['location']['latitude']
            longitude = data['data'][0]['location']['longitude']

        beaconResponse = BeaconResponse(beacon, beaconLikes, latitude, longitude)
        serializer = BeaconResponseSerializer(beaconResponse)
        return Response(serializer.data)