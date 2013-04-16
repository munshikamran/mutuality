from django.db import models
from facebookUserMatch import FacebookUserMatch

class FacebookUserMatchRating( models.Model ):
    match = models.ForeignKey(FacebookUserMatch)
    thumbsUp = models.NullBooleanField(null=True)

    class Meta:
        app_label = 'connect'

