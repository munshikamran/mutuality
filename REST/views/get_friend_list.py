from django.http import Http404
from connect.models import Profile
from REST.serializers import ProfileSerializer, FacebookUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.getFriendList import GetFriendList

class GetFriendsList(APIView):
    """
    Get the user's Friend List.
    """
    def get_object(self, pk, numFriends):
        try:
            profile = Profile.objects.get(facebookID=pk)
            numFriends = int(numFriends)
            if (numFriends == 0):
                facebookUserList = GetFriendList(profile)
            else:
                facebookUserList = GetFriendList(profile, numFriends)
            return facebookUserList
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        facebookUserList = self.get_object(request.DATA['token'], request.DATA['numFriends'])
        serializer = FacebookUserSerializer(facebookUserList)
        return Response(serializer.data)


