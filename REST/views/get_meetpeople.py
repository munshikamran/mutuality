from django.http import Http404
from connect.models import Profile
from REST.serializers import FacebookUserMeetPeopleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.functions import GetMeetPeople
from common.enums import MEET_PEOPLE_FILTER

class GetMeetPeopleAPI(APIView):
    """
    Get the user's meet people list, but only the fresh users for the Friendship filter.
    """
    def get_object(self, pk, viewed, dating):
        try:
            profile = Profile.objects.get(facebookID=pk)
            if (viewed == "0" and dating == "0"):
                facebookUserList = GetMeetPeople(profile, MEET_PEOPLE_FILTER.FRIENDSHIP)
                return facebookUserList.freshUsers
            elif (viewed == "1" and dating == "0"):
                facebookUserList = GetMeetPeople(profile, MEET_PEOPLE_FILTER.FRIENDSHIP)
                return facebookUserList.viewedUsers
            elif (viewed == "0" and dating == "1"):
                facebookUserList = GetMeetPeople(profile, MEET_PEOPLE_FILTER.DATING)
                return facebookUserList.freshUsers
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        facebookUserList = self.get_object(request.DATA['token'], request.DATA['viewed'], request.DATA['dating'])
        serializer = FacebookUserMeetPeopleSerializer(facebookUserList)
        return Response(serializer.data)
