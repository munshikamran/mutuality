from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from la_facebook.models import UserAssociation
import facebook	
from geopy import geocoders
from geopy import distance
# Create your models here.

class Profile(models.Model):
	user = models.ForeignKey(User)
	bio = models.TextField()
	name = models.CharField(max_length=255)
	age = models.IntegerField(default=-1)
	birthday = models.CharField(max_length =255, default='')
	location = models.CharField(max_length=255,default='') #can be a location from facebook or a zipcode
	gender = models.CharField(max_length=6, default='')
	interestedInMen = models.BooleanField(default=False)
	interestedInWomen = models.BooleanField(default=False)
	lookingForFriends = models.BooleanField(default=True)
	

	def authToken(self):
		return UserAssociation.objects.get(user_id=self.user.id).token
	def facebookID(self):
		return UserAssociation.objects.get(user_id=self.user.id).identifier
	def mutualFriends(self,otherProfile):
		graph = facebook.GraphAPI(self.authToken())
		friends = graph.get_connections("me","mutualfriends/"+otherProfile.facebookID())
		return friends
	def imageURL(self,type='normal'):
		url = 'http://graph.facebook.com/%s/picture?type=%s'
		return url % (self.facebookID(), type)
	def distanceToOther(self,otherProfile):
		g = geocoders.Google()
		loc1 = self.location
		_, coord = g.geocode(self.location)
		_, otherCoord = g.geocode(otherProfile.location)
		return distance.distance(coord,otherCoord).miles
	def locationFromFacebook(self):
		# other facts we can get http://developers.facebook.com/docs/reference/api/user/
		graph = facebook.GraphAPI(self.authToken())
		kwargs = {"fields": "location"}
		return graph.get_object("me",**kwargs)['location']['name']
	def updateInfoUsingFacebook(self):
		fields = ['location','birthday','interested_in','gender']
		graph = facebook.GraphAPI(self.authToken())
		kwargs = {"fields": fields}
		dictInfo = graph.get_object("me",**kwargs)
		if 'location' in dictInfo.keys():
			self.location = dictInfo['location']['name']
		if 'birthday' in dictInfo.keys():
			self.birthday = dictInfo['birthday']
		if 'interested_in' in dictInfo.keys():
			print 'interested_in needs to be completed'
			print dictInfo['interested_in']
		if 'gender' in dictInfo.keys():
			self.gender = dictInfo['gender']
		self.save()

	#getMatches calls
	def getMatches(self):
		#only return pairs with matchScore greater than 0
		q = Q(matchScore__gte=0) & (Q(profile1=self) | Q(profile2=self))
		#sort pairs by matchScore
		matchPairs = ProfilePair.objects.order_by('matchScore').filter(q)

		matches = []
		for matchPair in matchPairs:
			if matchPair.profile1 == self:
				matches.append(matchPair.profile2)
			else:
				matches.append(matchPair.profile1)
		return matches





class ProfilePair(models.Model):
	profile1 = models.ForeignKey(Profile, related_name='profile1')
	profile2 = models.ForeignKey(Profile, related_name='profile2')
	mutualFriendCount = models.IntegerField(default=0)
	distance = models.FloatField(default =float('inf'))
	matchScore = models.FloatField(default=0)
	
	def computeMatchScore(self):
		self.matchScore =  self.mutualFriendCount/(self.distance + 1)


# class MutualFriends(models.Model):
# 	mutualfriends_profile1 = models.ForeignKey(Profile, related_name='mutualfriends_profile1')
# 	mutualfriends_profile2 = models.ForeignKey(Profile, related_name='mutualfriends_profile2')
# 	number = models.IntegerField()


# class GeographicDistance(models.Model):
# 	distance_profile1 = models.ForeignKey(Profile, related_name='distance_profile1')
# 	distance_profile2 = models.ForeignKey(Profile, related_name='distance_profile2')
# 	distance = models.FloatField()