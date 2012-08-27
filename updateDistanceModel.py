import settings
import facebook
from django.contrib.auth.models import User
from django.db import models
from la_facebook.models import UserAssociation
from connect.models import GeographicDistance
from connect.models import Profile



profiles = Profile.objects.all()
for i in range(0,len(profiles)):
    profile1 = profiles[i]
    for j in range(i+1,len(profiles)):
        profile2 = profiles[j]
        distance = profile1.distanceToOther(profile2)
        dist = GeographicDistance(distance_profile1=profile1, distance_profile2=profile2, distance=distance)
        dist.save()
