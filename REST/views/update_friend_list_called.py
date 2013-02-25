from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.functions.updateFriendList import UpdateFriendListHasBeenCalled

class UpdateFriendListCalledAPI(APIView):
    '''
    Checks to see if the UpdateFriendList call has ever been made
    '''
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            success = UpdateFriendListHasBeenCalled(profile)
            return Response(success)
        except:
            raise Http404