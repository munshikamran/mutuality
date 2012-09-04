from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from la_facebook.models import UserAssociation
from messages.models import Message
import facebook	
from geopy import geocoders
from geopy import distance
import random
from datetime import datetime, timedelta
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
	# femaleFriendList = []
	# maleFriendList = []
	# maleLocationDictionary = {}
	# femaleLocationDictionary = {}
	# locationSet = ()

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


	# MESSAGE THREADS
	#imagine this working like facebook where user can see last few messages and clicking on the message opens the thread.
	#thus we will first call getRecentMessages and then when a message is selected we will call getMessageThreadWithOther
	#return all messages associated with profile that have been sent since past date
	def getMessagesSince(self,pastDate):
		q = (Q(sender_id=self.user_id) | Q(recipient_id=self.user_id)) & Q(sent_at__gte=pastDate)
		#order newer messages first
		return Message.objects.filter(q).order_by('sent_at').reverse()

	#return all messages associated with profile that have been sent in last month
	def getRecentMessages(self):
		now = datetime.now()
		pastDate = now - timedelta(weeks=4)
		return self.getMessagesSince(pastDate)

	def getMessageThreadWithOther(self,otherProfile):
		q = (Q(sender_id=self.user_id) & Q(recipient_id=otherProfile.user_id)) | (Q(sender_id=otherProfile.user_id) & Q(recipient_id=self.user_id))
		#order older messages first
		return Message.objects.filter(q).order_by('sent_at')

	#test function showing output of thread
	def outputThread(self,otherProfile):
		thread = self.getMessageThreadWithOther(otherProfile)
		if len(thread) == 0:
			return
		for m in thread:
			name = Profile.objects.get(user_id=m.sender_id).name
			content = m.body
			print name + ': ' + content




	# SITE USER MATCH MAKING
	def getMatchPairs(self):
		#only return pairs with matchScore greater than 0
		q = Q(matchScore__gte=0) & (Q(profile1=self) | Q(profile2=self))
		#sort pairs by matchScore greatest to smallest
		return ProfilePair.objects.filter(q).order_by('matchScore').reverse()

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
		year = datetime.now().year
		birthdayKey = 'birthday'
		ageKey = 'age'
		locationKey = 'location'
		stateKey = 'state'
		for friend in self.friendList:
			if birthdayKey in friend.keys():
				bday = friend[birthdayKey].split('/')
				# see if they share the year they were born
				if len(bday )== 3:
					yearBorn = int(bday[2])
					friend[ageKey] = year - yearBorn
			if locationKey in friend.keys():
				if friend[locationKey]['name'] != None:
					state = friend[locationKey]['name'].split(', ')[-1]
					friend[stateKey] = state



	# def updateGenderFriendLists(self):
	# 	if len(self.friendList) == 0:
	# 		self.updateFriendList()
	# 	for friend in self.friendList:
	# 		if 'gender' in friend.keys():
	# 			if friend['gender'] == 'female':
	# 				self.femaleFriendList.append(friend)
	# 			else:
	# 				self.maleFriendList.append(friend)

	# def updateLocationDictionaries(self):
	# 	if len(self.femaleFriendList) == 0 and len(self.maleFriendList) == 0:
	# 		self.updateGenderFriendLists()
	# 	for girl in self.femaleFriendList:
	# 		if 'location' in girl.keys():
	# 			locationName = girl['location']['name']
	# 			if not locationName in self.femaleLocationDictionary.keys():
	# 				self.femaleLocationDictionary[locationName] = []
	# 			self.femaleLocationDictionary[locationName].append(girl)
	# 	for guy in self.maleFriendList:
	# 		if 'location' in guy.keys():
	# 			locationName = guy['location']['name']
	# 			if not locationName in self.maleLocationDictionary.keys():
	# 				self.maleLocationDictionary[locationName] = []
	# 			self.maleLocationDictionary[locationName].append(guy)

	# def getRandomMatch(self):
	# 	if len(self.femaleFriendList) == 0 and len(self.maleFriendList) == 0:
	# 		self.updateGenderFriendLists()
	# 	numGirls = len(self.femaleFriendList)
	# 	numGuys = len(self.maleFriendList)
	# 	girlIDX = random.randint(0,numGirls-1)
	# 	guyIDX = random.randint(0,numGuys-1)
	# 	girl = self.femaleFriendList[girlIDX]
	# 	guy = self.maleFriendList[guyIDX]
	# 	print guy['name'] + ' and ' + girl['name'] + ' sitting in a tree'

	# def getRandomLocationMatch(self):
	# 	if len(self.maleLocationDictionary.keys()) == 0 and len(self.femaleLocationDictionary) == 0:
	# 		self.updateLocationDictionaries
	# 	if len(self.locationSet) == 0:
	# 		self.locationSet = set(self.maleLocationDictionary.keys()).intersection(set(self.femaleLocationDictionary.keys()))
	# 	#get random location
	# 	location = random.sample(self.locationSet,1)[0]
	# 	guys = self.maleLocationDictionary[location]
	# 	numGuys = len(guys)
	# 	guyIDX = random.randint(0,numGuys-1)
	# 	guy = guys[guyIDX]
	# 	girls = self.femaleLocationDictionary[location]
	# 	numGirls = len(girls)
	# 	girlIDX = random.randint(0,numGirls-1)
	# 	girl = girls[girlIDX]
	# 	matchFound = True
	# 	print guy['name'] + ' and ' + girl['name'] + ' from ' + str(location)

	def getRandomFriend(self):
		if len(self.friendList) == 0:
			self.updateFriendList()
		numFriends = len(self.friendList)
		friendIDX = random.randint(0,numFriends)
		return self.friendList[friendIDX]

	def getFriendMatchArgs(self,friend):
		args = []
		keys = friend.keys()
		if 'gender' in keys:
			args.append('gender')
		if 'location' in keys:
			# args.append('location')
			args.append('state')
		if 'age' in keys:
			args.append('age')
		return args

	def getFriendPotentials(self,friend,*args):
		potentials = []
		print args

		#check if friend even has args (if not no match can be made)
		for arg in args:
			if not arg in friend.keys():
				print "a match can not be made for "+ friend['name'] + ' based on the args'
				print args
				return potentials

		for otherFriend in self.friendList:
			isPotential = not friend == otherFriend
			#filter by gender
			if 'gender' in args:
				if friend['gender'] == 'female':
					desiredGender = 'male'
				else:
					desiredGender = 'female'
				isPotential = isPotential and 'gender' in otherFriend.keys() and (otherFriend['gender'] == desiredGender)
			#filter by location
			if 'location' in args:
				isPotential = isPotential and 'location' in otherFriend.keys() and (friend['location'] == otherFriend['location'])
			#filter by state
			if 'state' in args:
				isPotential = isPotential and 'state' in otherFriend.keys() and (friend['state'] == otherFriend['state'])
			#filter by age
			if 'age' in args:
				maxAgeDifference = 5
				isPotential = isPotential and 'age' in otherFriend.keys() and (abs(friend['age'] - otherFriend['age']) <= maxAgeDifference)

			if isPotential:
				potentials.append(otherFriend)
		return potentials

	def getFriendOptimumPotentials(self,friend):
		args = self.getFriendMatchArgs(friend)
		potentials = self.getFriendPotentials(friend,*args)
		return potentials

	def getMatchForFriendFromPotentials(self,friend,potentials):
		numPotentials = len(potentials)
		if numPotentials == 0:
			print 'no matches for ' + friend['name']
			return None
		else:
			idx = random.randint(0,numPotentials-1)
			return [friend,potentials[idx]]

	def getRandomMatch(self):
		friend = self.getRandomFriend()
		potentials = self.getFriendOptimumPotentials(friend)
		match = self.getMatchForFriendFromPotentials(friend,potentials)
		if match == None:
			print 'match not found'
		else:
			print match[0]['name'] + ' and ' + match[1]['name']
		return match



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

