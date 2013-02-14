from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.functions.getMessages import GetNewMessageCount


class GetNewMessageCountAPI(APIView):
    """
    Get the number of new messages a user has
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(facebookID=pk)
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        profile = self.get_object(request.DATA['token'])
        newMessageCount = GetNewMessageCount(profile)
        return Response(newMessageCount)
