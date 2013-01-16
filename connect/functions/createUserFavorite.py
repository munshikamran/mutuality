from connect.models import FacebookUser
from connect.models import UserFavorite

def CreateUserFavorite(profile,facebookUserID):
    try:
        facebookUser = FacebookUser.objects.get(facebookID = facebookUserID)
        userFavorite, created = UserFavorite.objects.get_or_create(
        user = profile, favorite = facebookUser)
        userFavorite.save()
        return True
    except:
        print "Unexpected error when creating User Favorite"
        return False

