from django.http import Http404
from connect.models import Profile
from REST.serializers import FacebookUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions import GetMeetPeople
from common.enums import MEET_PEOPLE_FILTER

class GetMeetPeopleViewedAPI(APIView):
    """
    Get the user's meet people list, but only the viewed users.
    """
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(facebookID=pk)
            facebookUserListViewed = GetMeetPeople(profile, MEET_PEOPLE_FILTER.FRIENDSHIP)
            return facebookUserListViewed
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        facebookUserListViewed = self.get_object(request.DATA['token'])
        serializer = FacebookUserSerializer(facebookUserListViewed.viewedUsers)
        return Response(serializer.data)
