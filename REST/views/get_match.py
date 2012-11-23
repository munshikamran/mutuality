from django.http import Http404
from Mutuality.connect.models import Profile
from REST.serializers import ProfileSerializer, FacebookUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.getMatches import GetNewMatch

class GetMatch(APIView):
    """
    Get a match.
    """
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            match = GetNewMatch(profile, request.DATA['gender1'], request.DATA['gender2'])
            serializer = FacebookUserSerializer([match.person1, match.person2])
            return Response(serializer.data)
        except Profile.DoesNotExist:
            raise Http404
