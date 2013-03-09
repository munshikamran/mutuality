from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.updateProfile import UpdateProfile

class SetProfileAPI(APIView):
    '''
    Sets/updates the user profile
    '''
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            success = UpdateProfile(profile, request.DATA['userData']);
            return Response(success)
        except:
            raise Http404