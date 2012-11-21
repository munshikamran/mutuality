from rest_framework import serializers
from Mutuality.connect.models.profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('facebookID', 'user', 'bio', 'name', 'age', 'birthday', 'location', 'gender')
