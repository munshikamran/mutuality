from connect.models import FacebookUser
from connect.models import UserFavorite
import sys

def RemoveUserFavorite(profile,facebookUserID):
    try:
        facebookUser = FacebookUser.objects.get(facebookID = facebookUserID)
        UserFavorite.objects.get(user = profile, favorite = facebookUser).delete()
        return True
    except:
        print "Unexpected error when creating User Favorite:", sys.exc_info()
        return False
