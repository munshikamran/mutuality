from django.db import models

class Beacon(models.Model):
    user = models.ForeignKey('Profile', related_name="beacon_by")
    place = models.CharField(max_length=255)
    activity = models.CharField(max_length=255)
    date_created = models.DateTimeField("Date Created", auto_now_add=True)

    class Meta:
        app_label = 'connect'

    def __unicode__(self):
        return "%s  %s" % ( self.user.name, self.place)