from django.contrib import admin
from django.conf import settings
from connect.models import Profile

if settings.DEBUG:
    admin.site.register(Profile)
