from django.db import models

class BeaconActivity(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('BeaconCategory', related_name="beacon_category")

    class Meta:
        app_label = 'connect'

    def __unicode__(self):
        return "%s %s" % (self.name, self.category.name)