from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response

from connect.functions.removeUserFavorite import RemoveUserFavorite

class RemoveFavoriteAPI(APIView):
    '''
    Removes a user favorite
    '''
    def post(self, request, format=None):
        try:
            profile = Profile.objects.get(facebookID=request.DATA['token'])
            success = RemoveUserFavorite(profile, request.DATA['facebookID']);
            return Response(success)
        except:
            raise Http404