from django.contrib import admin
from django.conf import settings
from connect.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name','location')


admin.site.register(Profile,ProfileAdmin)
