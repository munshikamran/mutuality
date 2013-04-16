from datetime import datetime
from django.db import models
from connect.models import Profile
from connect.models import FacebookUser
from connect.models import PotentialMatchUpdate
from connect.models.potentialBatch import PotentialBatch


class PotentialMatch(models.Model):
    profile = models.ForeignKey(Profile, related_name='potential_match_for')
    facebookUser = models.ForeignKey(FacebookUser, related_name='potential_match_with')
    potentialMatchBatch = models.ForeignKey(PotentialBatch, related_name='potential_match_batch', null=True)
    numMutualFriends = models.IntegerField()
    isMutualityConnection = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
            app_label = 'connect'