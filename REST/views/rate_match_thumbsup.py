from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.rateMatch import RateThumbsUp

class RateMatchThumbsUpAPI(APIView):
    '''
    Stores the thumbs up rating of a match
    '''
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            success = RateThumbsUp(profile, request.DATA['leftSlotFacebookID'], request.DATA['rightSlotFacebookID'])
            return Response(success)
        except:
            raise Http404