from django.db import models
from profile import Profile
from facebookuser import FacebookUser


# Create your models here.
class FacebookUserMatch( models.Model ):
    profile = models.ForeignKey(Profile)
    facebookUser1 = models.ForeignKey(FacebookUser, related_name="match_facebookUser1")
    facebookUser2 = models.ForeignKey(FacebookUser, related_name="match_facebookUser2")
    date_created = models.DateTimeField( "Date Created", auto_now_add=True )
    date_updated = models.DateTimeField( "Date Updated", auto_now=True )

    class Meta:
        app_label = 'connect'

    def __unicode__(self):
        return "%s : %s and %s" % ( self.profile, self.facebookUser1,self.facebookUser2 )
