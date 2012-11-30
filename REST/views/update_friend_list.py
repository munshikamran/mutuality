from django.http import Http404
from Mutuality.connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.updateFriendList import UpdateFriendList

class UpdateFriendListAPI(APIView):
    '''
    Contacts facebook to get users friend list and updates Mutualitys database with returned friend data
    '''
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            success = UpdateFriendList(profile)
            return Response(success)
        except:
            raise Http404