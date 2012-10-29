from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
import settings
from la_facebook.models import UserAssociation
from messages.models import Message
import facebook	
from geopy import geocoders
from geopy import distance
import random
from datetime import datetime, timedelta
from picklefield.fields import PickledObjectField

# Create your models here.
class FacebookUser( models.Model ):
    
    #id
    facebookID = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=-1)
    birthday = models.CharField(max_length =255, default='')
    location = models.CharField(max_length=255,default='') #can be a location from facebook or a zipcode
    gender = models.CharField(max_length=6, default='')
    single = models.BooleanField(default=False)
    interestedInMen = models.BooleanField(default=False)
    interestedInWomen = models.BooleanField(default=False)
    date_created = models.DateTimeField( "Date Created", auto_now_add=True )
    date_updated = models.DateTimeField( "Date Updated", auto_now=True )
    
    class Meta:
        app_label = 'connect'

    def __unicode__(self):
        return "%s  %s" % ( self.name, self.facebookID)


