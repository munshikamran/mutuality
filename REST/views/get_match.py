from django.http import Http404
from Mutuality.connect.models import Profile
from REST.serializers import ProfileSerializer, FacebookUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.getMatches import GetNewMatch, GetNewMatchIncludingPerson

class GetMatch(APIView):
    """
    Get a match.
    """
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            if request.DATA['leftSlotLocked'] == "true" and request.DATA['rightSlotLocked'] == "false":
                person = Profile.objects.get(facebookID=request.DATA['leftSlotID'])
                match = GetNewMatchIncludingPerson(profile, person, request.DATA['rightSlotGender'])
                serializer = FacebookUserSerializer([match.person1, match.person2])
                return Response(serializer.data)
            elif request.DATA['leftSlotLocked'] == "false" and request.DATA['rightSlotLocked'] == "true":
                person = Profile.objects.get(facebookID=request.DATA['rightSlotID'])
                match = GetNewMatchIncludingPerson(profile, person, request.DATA['leftSlotGender'])
                serializer = FacebookUserSerializer([match.person1, match.person2])
                return Response(serializer.data)
            else:
                match = GetNewMatch(profile, request.DATA['leftSlotGender'], request.DATA['rightSlotGender'])
                serializer = FacebookUserSerializer([match.person1, match.person2])
                return Response(serializer.data)
        except Profile.DoesNotExist:
            raise Http404
