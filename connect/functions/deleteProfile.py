from django.contrib.auth.models import User
from connect.models import Profile
from connect
def DeleteProfile(profile):
    user = profile.user.delete()
    profile.delete()

