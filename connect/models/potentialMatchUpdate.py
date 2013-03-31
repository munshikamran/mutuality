from datetime import datetime
from django.db import models
from connect.models import Profile


class PotentialMatchUpdate(models.Model):
    profile = models.ForeignKey(Profile, related_name='potential_match_update_for')
    date_made = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'connect'
