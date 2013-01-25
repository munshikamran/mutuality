from django.http import Http404
from connect.models import Profile
from REST.serializers import FacebookUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions import GetMeetPeople
from common.enums import MEET_PEOPLE_FILTER

class GetMeetPeopleAPI(APIView):
    """
    Get the user's meet people list.
    """
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(facebookID=pk)
            facebookUserList = GetMeetPeople(profile, MEET_PEOPLE_FILTER.FRIENDSHIP)
            return facebookUserList.freshUsers
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        facebookUserList = self.get_object(request.DATA['token'])
        serializer = FacebookUserSerializer(facebookUserList)
        return Response(serializer.data)
