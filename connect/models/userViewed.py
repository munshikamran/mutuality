from django.db import models
from facebookuser import FacebookUser
from profile import Profile
class UserViewed( models.Model ):
    user = models.ForeignKey('Profile', related_name="viewed_by" )
    viewed = models.ForeignKey(FacebookUser, related_name="viewed_person")
    date_last_viewed = models.DateTimeField( "Date Last Viewed", auto_now=True )

    class Meta:
        app_label = 'connect'

    def __unicode__(self):
        return "%s was viewed by %s" % ( self.viewed, self.user )
