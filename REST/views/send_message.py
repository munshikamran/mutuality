from django.http import Http404
from connect.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.functions.sendMessage import SendMessage


class SendMessageAPI(APIView):
    """
    Send a message to another user
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(facebookID=pk)
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        profile = self.get_object(request.DATA['token'])
        otherFbId = request.DATA['otherFbId']
        messageContent = request.DATA['messageContent']
        success = SendMessage(profile, otherFbId, messageContent)
        return Response(success)