from django.http import Http404
from connect.models import Profile
from REST.serializers import MeetPeopleProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions import GetMeetPeopleProfile

class GetMeetPeopleProfileAPI(APIView):
    """
    Get a person's extra facebook information.
    """
    def get_object(self, pk):
        try:
            meetPeopleProfile = GetMeetPeopleProfile(pk)
            return meetPeopleProfile
        except:
            raise Http404

    def post(self, request, format=None):
        meetPeopleProfile = self.get_object(request.DATA['facebookID'])
        serializer = MeetPeopleProfileSerializer(meetPeopleProfile)
        return Response(serializer.data)
