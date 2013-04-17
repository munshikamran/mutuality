from django.db import models

class BeaconCategory(models.Model):
    name = models.CharField(max_length=255)
    picture_url = models.CharField(max_length=255)

    class Meta:
        app_label = 'connect'

    def __unicode__(self):
        return "%s" % (self.name)