from django.contrib.auth.models import User
from connect.models import Profile


def DeleteProfile(profile):
    user = profile.user.delete()
    profile.delete()

