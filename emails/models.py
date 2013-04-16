from django.db import models
from django.contrib.auth.models import User


class Email(models.Model):
    WELCOME = 'WE'
    FRIEND_JOINED = 'FJ'
    USER_INACTIVE = 'UI'
    EMAIL_TYPE_CHOICES = (
        (WELCOME, 'Welcome'),
        (FRIEND_JOINED, 'Friend Joined'),
        (USER_INACTIVE, 'User Inactive'),
    )
    user = models.ForeignKey(User, related_name='+') #we don't need to user model to have a relation back to this model
    subject = models.CharField(max_length=120)
    text_body = models.TextField()
    html_body = models.TextField()
    to_address = models.EmailField()
    from_address = models.EmailField()
    email_type = models.CharField(max_length=2, choices=EMAIL_TYPE_CHOICES)
    sent_at = models.DateTimeField(auto_now=True)