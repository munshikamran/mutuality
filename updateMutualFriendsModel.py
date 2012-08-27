import settings
import facebook
from django.contrib.auth.models import User
from django.db import models
from la_facebook.models import UserAssociation
from connect.models import MutualFriends
from connect.models import Profile



profiles = Profile.objects.all()
for i in range(0,len(profiles)):
    profile1 = profiles[i]
    graph = facebook.GraphAPI(profile1.authToken())
    for j in range(i+1,len(profiles)):
        profile2 = profiles[j]
        friends = profile1.mutualFriends(profile2)
        #print friends['data']
        numFriends = len(friends['data'])
        m = MutualFriends(mutualfriends_profile1=profile1, mutualfriends_profile2=profile2, number=numFriends)
        m.save()
