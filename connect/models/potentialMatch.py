from datetime import datetime
from django.db import models
from connect.models import Profile
from connect.models import FacebookUser
from connect.models import PotentialMatchUpdate

class PotentialMatch(models.Model):
    profile = models.ForeignKey(Profile, related_name='potential_match_for')
    facebookUser = models.ForeignKey(FacebookUser, related_name='potential_match_with')
    potentialMatchUpdate = models.ForeignKey(PotentialMatchUpdate)
    numMutualFriends = models.IntegerField()
    isMutualityConnection = models.BooleanField(default=False)

    class Meta:
        app_label = 'connect'