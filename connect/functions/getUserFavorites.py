from connect.models import UserFavorite

def GetUserFavorites(profile):
#    get favorites for this user. Order so that most recently favorited users appear first in array
    try:
        favoritesOfProfile = UserFavorite.objects.filter(user=profile).order_by('date_created').reverse()
        return favoritesOfProfile
    except:
        print "Unexpected error when fetching user favorites"
        return False