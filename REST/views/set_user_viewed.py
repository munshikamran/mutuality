from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.viewUser import ViewUser
from common.enums.meetPeopleFilters import MEET_PEOPLE_FILTER

class SetUserViewedAPI(APIView):
    '''
    Set a user as viewed
    '''
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            success = ViewUser(profile, request.DATA['facebookID'], MEET_PEOPLE_FILTER.FRIENDSHIP);
            return Response(success)
        except:
            raise Http404