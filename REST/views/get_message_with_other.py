from django.http import Http404
from connect.models import Profile
from REST.serializers import MessagesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.functions.getMessages import GetMessageThreadWithOther


class GetMessageThreadWithOtherAPI(APIView):
    """
    Get the messages of this profile with another user
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(facebookID=pk)
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        profile = self.get_object(request.DATA['token'])
        otherFacebookID = request.DATA['facebookID']
        messages = GetMessageThreadWithOther(profile, otherFacebookID)
        serializer = MessagesSerializer(messages)
        return Response(serializer.data)
