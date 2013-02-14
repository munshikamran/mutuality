from django.http import Http404
from connect.models import Profile
from REST.serializers import MessagesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from connect.functions.getMessages import GetAllThreadPreviews


class GetThreadPreviewsAPI(APIView):
    """
    Get the threads previews to populate the user's inbox
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(facebookID=pk)
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        profile = self.get_object(request.DATA['token'])
        messages = GetAllThreadPreviews(profile)
        serializer = MessagesSerializer(messages)
        return Response(serializer.data)
