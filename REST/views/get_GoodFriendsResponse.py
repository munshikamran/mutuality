from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from REST.serializers import GoodFriendsResponseSerializer
from connect.functions.getGoodFriends import GetGoodFriendsForInvites
from connect.classes.goodFriendsResponse import GoodFriendsResponse

class GetGoodFriendsAPI(APIView):

    def get_GoodFriends(self, fbID, limit):
        try:
            profile = Profile.objects.get(facebookID=fbID)
            GoodFriends = GetGoodFriendsForInvites(profile, limit)
            return GoodFriends
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        print request.DATA['token']
        print request.DATA['lim']
        GoodFriends = self.get_GoodFriends(request.DATA['token'], request.DATA['lim'])
        print GoodFriends
        goodFriendsResponse = GoodFriendsResponse(GoodFriends.goodFriends, GoodFriends.numFriends, GoodFriends.numPotentialMatches)
        print goodFriendsResponse
        serializer = GoodFriendsResponseSerializer(goodFriendsResponse)
        return Response(serializer.data)