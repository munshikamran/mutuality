from django.db import models
from connect.models.facebookuser import FacebookUser
from connect.models.facebookUserMatch import FacebookUserMatch
from common.enums import MATCH_REASONS


class FacebookUserMatchReason(models.Model):
    match = models.ForeignKey(FacebookUserMatch)
    subject = models.ForeignKey(FacebookUser, related_name="reason_subject")
    object = models.ForeignKey(FacebookUser, related_name="reason_object")
    reason = models.CharField(max_length=255,choices=MATCH_REASONS.ENUM)

    class Meta:
        app_label = 'connect'