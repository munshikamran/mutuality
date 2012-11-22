from django.http import Http404
from Mutuality.connect.models import Profile
from REST.serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions import GetFriendList

class GetFriendList(APIView):
    """
    Get the user's Friend List.
    """
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(facebookID=pk)
            return GetFriendList(profile)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        friend_list = self.get_object(request.DATA['token'])
        serializer = ProfileSerializer(friend_list)
        return Response(serializer.data)


