from django.http import Http404
from Mutuality.connect.models import Profile
from REST.serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class GetProfile(APIView):
    """
    Get the user's Profile.
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(facebookID=pk)
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        profile = self.get_object(request.DATA['token'])
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    """
    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """


