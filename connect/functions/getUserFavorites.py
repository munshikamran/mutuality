from connect.models import UserFavorite
from connect.models import FacebookUser

def GetUserFavorites(profile):
#    get favorites for this user. Order so that most recently favorited users appear first in array
    try:
        favoritesOfProfile = UserFavorite.objects.select_related('favorite').filter(user=profile).order_by('date_created').reverse()
        facebookUsers = []
        for favorite in favoritesOfProfile:
            facebookUsers.append(favorite.favorite)

        return facebookUsers
    except:
        print "Unexpected error when fetching user favorites"
        return False