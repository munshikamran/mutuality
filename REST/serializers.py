from rest_framework import serializers
from connect.models.profile import Profile
from connect.models.friendship import Friendship
from connect.models.facebookuser import FacebookUser
from connect.models.userFavorite import UserFavorite
from messages.models import Message

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('facebookID', 'user', 'bio', 'name', 'birthdayString', 'birthdayDate', 'location', 'state', 'gender', 'relationshipStatus', "date_created", "date_updated")

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('user', 'friend')

class FacebookUserMeetPeopleSerializer(serializers.Serializer):
    facebookID = serializers.CharField()
    name = serializers.CharField()
    birthdayString = serializers.DateTimeField()
    location = serializers.CharField()
    state = serializers.CharField()
    gender = serializers.CharField()
    relationshipStatus = serializers.CharField()
    date_created = serializers.DateTimeField()
    date_updated = serializers.DateTimeField()
    isMutualityUser = serializers.BooleanField()

class FacebookUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookUser
        fields = ('facebookID', 'name', 'birthdayString', 'birthdayDate', 'location', 'state', 'gender', 'relationshipStatus', "date_created", "date_updated")


class MeetPeopleProfileSerializer(serializers.Serializer):
    gender = serializers.Field()
    relationshipStatus = serializers.Field()
    college = serializers.Field()
    age = serializers.Field()
    location = serializers.Field()
    employer = serializers.Field()

class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavorite
        fields = ('user', 'favorite', 'date_created')

class MessagesSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()
    recipient = ProfileSerializer()
    class Meta:
            model = Message
            fields = ('subject', 'body', 'recipient', 'sender', 'parent_msg', 'sent_at', 'read_at', 'replied_at', 'sender_deleted_at', 'recipient_deleted_at')


