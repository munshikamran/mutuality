from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.classes.matchRatingReason import MatchRatingReason

from connect.functions.rateMatch import RateThumbsDown

class RateMatchThumbsDownAPI(APIView):
    '''
    Stores the thumbs down rating of a match and the reasons why
    '''
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            numReasons = int(request.DATA['numReasons']);
            reasons = []
            for i in range (0, numReasons):
                mrr = MatchRatingReason(str(request.DATA['reasons['+str(i)+'][subject]']), str(request.DATA['reasons['+str(i)+'][object]']), str(request.DATA['reasons['+str(i)+'][enum]']))
                reasons.append(mrr);

            success = RateThumbsDown(profile, request.DATA['leftSlotFacebookID'], request.DATA['rightSlotFacebookID'], reasons)
            return Response(success)
        except:
            raise Http404