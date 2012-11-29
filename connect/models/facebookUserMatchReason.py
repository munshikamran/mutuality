from django.db import models
from facebookUserMatch import FacebookUserMatch

class FacebookUserReason( models.Model ):
    match = models.ForeignKey(FacebookUserMatch)
    reason = models.CharField(max_length=255)

    class Meta:
        app_label = 'connect'