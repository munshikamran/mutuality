from rest_framework import serializers
from Mutuality.connect.models.profile import Profile
from Mutuality.connect.models.friendship import Friendship
from Mutuality.connect.models.facebookuser import FacebookUser

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('facebookID', 'user', 'bio', 'name', 'birthdayString', 'birthdayDate', 'location', 'state', 'gender', 'relationshipStatus', "date_created", "date_updated")

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('user', 'friend')

class FacebookUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookUser
        fields = ('facebookID', 'name', 'birthdayString', 'birthdayDate', 'location', 'state', 'gender', 'relationshipStatus', "date_created", "date_updated")

