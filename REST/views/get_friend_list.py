from django.http import Http404
from connect.models import Profile
from REST.serializers import ProfileSerializer, FacebookUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions import GetFriendList

class GetFriendsList(APIView):
    """
    Get the user's Friend List.
    """
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(facebookID=pk)
            facebookUserList = GetFriendList(profile)
            return facebookUserList
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        facebookUserList = self.get_object(request.DATA['token'])
        serializer = FacebookUserSerializer(facebookUserList)
        return Response(serializer.data)


