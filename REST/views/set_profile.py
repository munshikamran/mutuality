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
            pfDict = {}
            print request.DATA['location']
            print request.DATA['relationship_status']
            print request.DATA['gender']
            pfDict['location'] = {}
            pfDict['location']['name'] = request.DATA['location']
            pfDict['relationship_status'] = request.DATA['relationship_status']
            pfDict['gender'] = request.DATA['gender']
            success = UpdateProfile(profile, pfDict)
            return Response(success)
        except:
            raise Http404