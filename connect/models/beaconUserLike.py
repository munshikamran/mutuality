from django.db import models

class BeaconUserLike(models.Model):
    user = models.ForeignKey('Profile', related_name="beacon_liked_by")
    beacon = models.ForeignKey('Beacon', related_name="beacon_liked")

    class Meta:
        app_label = 'connect'

    def __unicode__(self):
        return "%s  %s" % ( self.user.name, self.beacon)