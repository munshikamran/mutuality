from connect.models import Profile
from la_facebook.models import UserAssociation

def GetProfileAuthToken(profile):
    return UserAssociation.objects.get(user_id=profile.user.id).token