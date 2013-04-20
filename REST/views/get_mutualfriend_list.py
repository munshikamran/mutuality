from django.http import Http404
from connect.models import Profile
from REST.serializers import FacebookUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.getMutualFriendList import GetMutualFriendListWithFacebookUserID

class GetMutualFriendListAPI(APIView):
    """
    Get the user's meet people list.
    """
    def get_object(self, pk, fbID):
        try:
            profile = Profile.objects.get(facebookID=pk)
            mutualUserList = GetMutualFriendListWithFacebookUserID(profile, fbID)
            return mutualUserList
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        mutualUserList = self.get_object(request.DATA['token'], request.DATA['facebookID'])
        serializer = FacebookUserSerializer(mutualUserList)
        return Response(serializer.data)
