import settings
import facebook
from django.contrib.auth.models import User
from django.db import models
from la_facebook.models import UserAssociation
from connect.models import ProfilePair
from connect.models import Profile



profiles = Profile.objects.all()
for i in range(0,len(profiles)):
    profile1 = profiles[i]
    graph = facebook.GraphAPI(profile1.authToken())
    for j in range(i+1,len(profiles)):
        profile2 = profiles[j]
        friends = profile1.mutualFriends(profile2)
        numFriends = len(friends['data'])
        distance = float("inf")
        if numFriends > 0:
        	distance = profile1.distanceToOther(profile2)

        #if already in database, update
        profileList = ProfilePair.objects.filter(profile1=profile1,profile2=profile2)
        if len(profileList) == 0:
            profileList = ProfilePair.objects.filter(profile1=profile2,profile2=profile1)
        if len(profileList) > 0:
            m = profileList[0]
            m.mutualFriendCount = numFriends
            m.distance = distance
        #if not create new object
        else:
            m = ProfilePair(profile1=profile1, profile2=profile2, mutualFriendCount=numFriends, distance=distance)
        m.computeMatchScore()
        if m.matchScore > 0:
            m.save()
