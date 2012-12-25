from django.http import Http404
from Mutuality.connect.models import Profile
from REST.serializers import FacebookUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions import GetFriendsOfFriends

class GetFriendsOfFriendsList(APIView):
    """
    Get the user's Friend of friend list.
    """
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(facebookID=pk)
            facebookUserList = GetFriendsOfFriends(profile)
            return facebookUserList
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        facebookUserList = self.get_object(request.DATA['token'])
        serializer = FacebookUserSerializer(facebookUserList)
        return Response(serializer.data)
