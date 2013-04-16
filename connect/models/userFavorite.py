from django.db import models
from facebookuser import FacebookUser

class UserFavorite( models.Model ):
    user = models.ForeignKey('Profile', related_name="favorite_of" )
    favorite = models.ForeignKey(FacebookUser, related_name="favorite_person")
    date_created = models.DateTimeField( "Date Created", auto_now_add=True )

    class Meta:
        app_label = 'connect'

    def __unicode__(self):
        return "%s is a favorite of %s" % ( self.favorite, self.user )