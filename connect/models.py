from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from la_facebook.models import UserAssociation
import facebook	
from geopy import geocoders
from geopy import distance
import random
import datetime
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

	# fields we don't store in the database
	friendList= []
	femaleFriendList = []
	maleFriendList = []
	maleLocationDictionary = {}
	femaleLocationDictionary = {}
	locationSet = ()

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
		graph = facebook.GraphAPI(self.authToken())
		fields = ['location','birthday','interested_in','gender']
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
	def getMatchPairs(self):
		#only return pairs with matchScore greater than 0
		q = Q(matchScore__gte=0) & (Q(profile1=self) | Q(profile2=self))
		#sort pairs by matchScore greatest to smallest
		return ProfilePair.objects.order_by('matchScore').reverse().filter(q)

	def getMatchProfiles(self):
		matchPairs = self.getMatchPairs()
		matches = []
		for matchPair in matchPairs:
			if matchPair.profile1 == self:
				matches.append(matchPair.profile2)
			else:
				matches.append(matchPair.profile1)
		return matches

	#FACEBOOK FRIEND MATCHMAKING METHODS
	def updateFriendList(self):
		graph = facebook.GraphAPI(self.authToken())
		fields = ['name','location','picture','gender','birthday']
		kwargs = {"fields": fields}
		self.friendList = graph.get_connections("me","friends",**kwargs)['data']
		# update friend ages
		year = datetime.datetime.now().year
		birthdayKey = 'birthday'
		ageKey = 'age'
		for friend in self.friendList:
			if birthdayKey in friend.keys():
				bday = friend[birthdayKey].split('/')
				# see if they share the year they were born
				if len(bday )== 3:
					yearBorn = int(bday[2])
					friend[ageKey] = year - yearBorn



	def updateGenderFriendLists(self):
		if len(self.friendList) == 0:
			self.updateFriendList()
		for friend in self.friendList:
			if 'gender' in friend.keys():
				if friend['gender'] == 'female':
					self.femaleFriendList.append(friend)
				else:
					self.maleFriendList.append(friend)

	def updateLocationDictionaries(self):
		if len(self.femaleFriendList) == 0 and len(self.maleFriendList) == 0:
			self.updateGenderFriendLists()
		for girl in self.femaleFriendList:
			if 'location' in girl.keys():
				locationName = girl['location']['name']
				if not locationName in self.femaleLocationDictionary.keys():
					self.femaleLocationDictionary[locationName] = []
				self.femaleLocationDictionary[locationName].append(girl)
		for guy in self.maleFriendList:
			if 'location' in guy.keys():
				locationName = guy['location']['name']
				if not locationName in self.maleLocationDictionary.keys():
					self.maleLocationDictionary[locationName] = []
				self.maleLocationDictionary[locationName].append(guy)

	def getRandomMatch(self):
		if len(self.femaleFriendList) == 0 and len(self.maleFriendList) == 0:
			self.updateGenderFriendLists()
		numGirls = len(self.femaleFriendList)
		numGuys = len(self.maleFriendList)
		girlIDX = random.randint(0,numGirls-1)
		guyIDX = random.randint(0,numGuys-1)
		girl = self.femaleFriendList[girlIDX]
		guy = self.maleFriendList[guyIDX]
		print guy['name'] + ' and ' + girl['name'] + ' sitting in a tree'

	def getRandomLocationMatch(self):
		if len(self.maleLocationDictionary.keys()) == 0 and len(self.femaleLocationDictionary) == 0:
			self.updateLocationDictionaries
		if len(self.locationSet) == 0:
			self.locationSet = set(self.maleLocationDictionary.keys()).intersection(set(self.femaleLocationDictionary.keys()))
		#get random location
		location = random.sample(self.locationSet,1)[0]
		guys = self.maleLocationDictionary[location]
		numGuys = len(guys)
		guyIDX = random.randint(0,numGuys-1)
		guy = guys[guyIDX]
		girls = self.femaleLocationDictionary[location]
		numGirls = len(girls)
		girlIDX = random.randint(0,numGirls-1)
		girl = girls[girlIDX]
		matchFound = True
		print guy['name'] + ' and ' + girl['name'] + ' from ' + str(location)



class ProfilePair(models.Model):
	profile1 = models.ForeignKey(Profile, related_name='profile1')
	profile2 = models.ForeignKey(Profile, related_name='profile2')
	mutualFriendCount = models.IntegerField(default=0)
	distance = models.FloatField(default =float('inf'))
	matchScore = models.FloatField(default=0)
	
	def computeMatchScore(self):
		self.matchScore =  self.mutualFriendCount/(self.distance + 1)


class ProfilePairRating(models.Model):
	rater = models.ForeignKey(Profile, related_name='rater')
	ratingProfile1 = models.ForeignKey(Profile, related_name='ratingProfile1')
	ratingProfile2 = models.ForeignKey(Profile, related_name='ratingProfile2')
	rating = models.IntegerField(default=0)


# class MutualFriends(models.Model):
# 	mutualfriends_profile1 = models.ForeignKey(Profile, related_name='mutualfriends_profile1')
# 	mutualfriends_profile2 = models.ForeignKey(Profile, related_name='mutualfriends_profile2')
# 	number = models.IntegerField()


# class GeographicDistance(models.Model):
# 	distance_profile1 = models.ForeignKey(Profile, related_name='distance_profile1')
# 	distance_profile2 = models.ForeignKey(Profile, related_name='distance_profile2')
# 	distance = models.FloatField()