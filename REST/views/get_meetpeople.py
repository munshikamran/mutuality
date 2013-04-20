from django.http import Http404
from connect.models import Profile
from REST.serializers import MeetPeopleResponseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.functions.getMeetPeople import GetMeetPeople
from common.enums import MEET_PEOPLE_FILTER

class GetMeetPeopleAPI(APIView):
    """
    Get the user's meet people list (for various filters) in addition to timestamp for when that list expires
    """
    def get_object(self, pk, viewed, dating, favorites):
        try:
            profile = Profile.objects.get(facebookID=pk)
            if (viewed == "0" and dating == "0" and favorites == "0"):
                meetPeopleResponse = GetMeetPeople(profile, MEET_PEOPLE_FILTER.FRIENDSHIP)
                return meetPeopleResponse
            elif (viewed == "1" and dating == "0" and favorites == "0"):
                meetPeopleResponse = GetMeetPeople(profile, MEET_PEOPLE_FILTER.VIEWED)
                return meetPeopleResponse
            elif (viewed == "0" and dating == "1" and favorites == "0"):
                meetPeopleResponse = GetMeetPeople(profile, MEET_PEOPLE_FILTER.DATING)
                return meetPeopleResponse
            elif (viewed == "0" and dating == "0" and favorites == "1"):
                meetPeopleResponse = GetMeetPeople(profile, MEET_PEOPLE_FILTER.FAVORITES)
                return meetPeopleResponse
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        meetPeopleResponse = self.get_object(request.DATA['token'], request.DATA['viewed'], request.DATA['dating'], request.DATA['favorites'])
        serializer = MeetPeopleResponseSerializer(meetPeopleResponse)
        return Response(serializer.data)
