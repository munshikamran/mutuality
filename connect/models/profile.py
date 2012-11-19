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

from facebookuser import FacebookUser
from friendship import Friendship

from common.enums import RELATIONSHIP_STATUS
from common.enums import GENDER

# Create your models here.
class Profile(models.Model):

	facebookID = models.CharField(max_length=255,primary_key=True)
	user = models.ForeignKey(User)
	bio = models.TextField()
	name = models.CharField(max_length=255)
	birthdayString = models.CharField(max_length =255,null=True)
	birthdayDate = models.DateTimeField(null=True)
	location = models.CharField(max_length=255,null=True) #can be a location from facebook or a zipcode
	state = models.CharField(max_length=255,null=True)
	gender = models.CharField(max_length=6,choices=GENDER.ENUM,null=True)
	relationshipStatus = models.CharField(max_length=255,choices=RELATIONSHIP_STATUS.ENUM,null=True)
	date_created = models.DateTimeField( "Date Created", auto_now_add=True )
	date_updated = models.DateTimeField( "Date Updated", auto_now=True )

	class Meta:
		app_label = 'connect'


	def updateUsingFacebookDictionary(self,fbDictionary):
		nameKey = 'name'
		if nameKey in fbDictionary.keys():
			  self.name = fbDictionary[nameKey]
		# update gender
		genderKey = 'gender'
		if genderKey in fbDictionary.keys():
			gender = fbDictionary[genderKey]
			# store as 'm' or 'f' not as 'male' or 'female'
			self.gender = gender

	# update age
		birthdayKey = 'birthday'
		if birthdayKey in fbDictionary.keys():
			bday = fbDictionary[birthdayKey].split('/')
			self.birthdayString = bday
			# birthday must include year for us to calculate age
			if len(bday)==3:
				self.birthdayDate = datetime(int(bday[2]),int(bday[0]),int(bday[1]))

		# update location
		locationKey = 'location'
		if locationKey in fbDictionary.keys() and not (fbDictionary[locationKey]['name'] == None):
			self.location = fbDictionary[locationKey]['name']
			state = fbDictionary[locationKey]['name'].split(', ')[-1]
			self.state = state
		# update relationship status
		relationshipStatusKey = 'relationship_status'
		if relationshipStatusKey in fbDictionary.keys():
			self.relationshipStatus = fbDictionary[relationshipStatusKey]

		self.save()

	def authToken(self):
		return UserAssociation.objects.get(user_id=self.user.id).token

#	def facebookID(self):
#		return UserAssociation.objects.get(user_id=self.user.id).identifier

	def mutualFriends(self,otherProfile):
		graph = facebook.GraphAPI(self.authToken())
		friends = graph.get_connections("me","mutualfriends/"+otherProfile.facebookID())
		return friends

	def imageURL(self,type='normal'):
		url = 'http://graph.facebook.com/%s/picture?type=%s'
		return url % (self.facebookID, type)

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


	# MESSAGE THREADS
	#imagine this working like facebook where user can see last few messages and clicking on the message opens the thread.
	#thus we will first call getRecentMessages and then when a message is selected we will call getMessageThreadWithOther
	#return all messages associated with profile that have been sent since past date

	def getMessagesSince(self,pastDate):
		q = Q(sender_deleted_at__isnull=True) & (Q(sender_id=self.user_id) | Q(recipient_id=self.user_id)) & Q(sent_at__gte=pastDate)
		#order newer messages first
		return Message.objects.filter(q).order_by('sent_at').reverse()

	#return all messages associated with profile that have been sent in last month
	def getRecentMessages(self):
		now = datetime.now()
		pastDate = now - timedelta(weeks=4)
		return self.getMessagesSince(pastDate)

	def getMessageThreadWithOther(self,otherProfile):
		q =  Q(sender_deleted_at__isnull=True) & (Q(sender_id=self.user_id) & Q(recipient_id=otherProfile.user_id)) | (Q(sender_id=otherProfile.user_id) & Q(recipient_id=self.user_id))
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

	#see messages.forms to make sure you are doing everything you want		
	def sendMessageToOtherProfile(self,otherProfile,messageBody):
		sender = self.user
		recipient = otherProfile.user
		body = messageBody
		message = Message(sender = sender, recipient = recipient,body = body)
		message.save()

	# FACEBOOK MESSAGING BETWEEN FRIENDS
	# https://developers.facebook.com/docs/reference/dialogs/send/
	def getMessageDialogueURLForFriend(self,friend,messageBody):
		urlRoot = 'https://www.facebook.com/dialog/send?'
		prop = {}
		prop['app_id'] = settings.FACEBOOK_APP_ID
		prop['redirect_uri'] = 'http://localhost:8000/'
		prop['to'] = friend['id']
		prop['link'] = 'www.mutuality.com'
		prop['description'] = messageBody
		url = urlRoot
		keys = prop.keys()
		for key in keys[0:len(keys)-1]:
			url +=  key + '=' + prop[key] + '&'
		key = keys[-1]
		url += key + '=' + prop[key]
		return url   

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
		now = datetime.now()
		yesterday = now - timedelta(days=1)
		# if self.friendList == '' or self.friendListLastUpdate < yesterday:
		if True:
			graph = facebook.GraphAPI(self.authToken())
			fields = ['name','location','picture','gender','birthday','relationship_status']
			kwargs = {"fields": fields}
			friendList = graph.get_connections("me","friends",**kwargs)['data']
			# update friend ages
			year = datetime.now().year
			birthdayKey = 'birthday'
			ageKey = 'age'
			locationKey = 'location'
			stateKey = 'state'
			for friend in friendList:
				if birthdayKey in friend.keys():
					bday = friend[birthdayKey].split('/')
					# see if they share the year they were born
					if len(bday )== 3:
						yearBorn = int(bday[2])
						friend[ageKey] = year - yearBorn
						# birthdate = datetime(bday[2],bday[0],bday[1])
						# now = datetime.now()
						# age = (now-birthdate).days/365.25

				if locationKey in friend.keys():
					if friend[locationKey]['name'] != None:
						state = friend[locationKey]['name'].split(', ')[-1]
						friend[stateKey] = state
				# set large image url
				friend['picture']['data']['largePicURL'] = 'https://graph.facebook.com/'+friend['id']+'/picture?type=large'
				# friend['picture']['data']['squarePicURL'] = 'https://graph.facebook.com/'+friend['id']+'/picture?width=250&height=250'
				# set profile url
				friend['facebookprofile'] = 'https://facebook.com/'+friend['id']
				# update if existing
				if FacebookUser.objects.filter(facebookID=friend['id']).exists():
					fbUser = FacebookUser.objects.get(facebookID=friend['id'])
					fbUser.updateUsingFacebookDictionary(friend)
					fbUser.save()
					# create a friendship if one doesn't exist
					if not Friendship.objects.filter(user=self,friend=fbUser).exists():
						friendship = Friendship(user=self,friend=fbUser)
						friendship.save()

				# else create new facebookuser
				else:
					fbUser = FacebookUser(facebookID=friend['id'],name=friend['name'])
					fbUser.updateUsingFacebookDictionary(friend)
					fbUser.save()
					# create friend relationship
					friendship = Friendship(user=self,friend=fbUser)
					friendship.save()

			self.friendList = friendList
			self.friendListLastUpdate = now
			self.save()


	def getRandomFriend(self):
		# if len(self.friendList) == 0:
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
			#check if pair has already been rated
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

	def rateFacebookMatch(self,match,rating):
		fbPairRating = FacebookPairRating(facebookPairRater=self,friendFacebookID1=match[0]['id'],friendFacebookID2=match[1]['id'],rating=rating)
		fbPairRating.save()

	def getFriendsFromDatabase(self):
		friendships =  list(Friendship.objects.filter(user=self).values_list('friend'))
		friendshipList=[]
		for friendship in friendships:
			friendshipList.append(friendship[0])
		return FacebookUser.objects.filter(facebookID__in=friendshipList)



class ProfilePair(models.Model):
	profile1 = models.ForeignKey(Profile, related_name='profile1')
	profile2 = models.ForeignKey(Profile, related_name='profile2')
	mutualFriendCount = models.IntegerField(default=0)
	distance = models.FloatField(default =float('inf'))
	matchScore = models.FloatField(default=0)

	def computeMatchScore(self):
		self.matchScore =  self.mutualFriendCount/(self.distance + 1)


class ProfilePairRating(models.Model):
	profilePairRater = models.ForeignKey(Profile, related_name='profilePairRater')
	ratingProfile1 = models.ForeignKey(Profile, related_name='ratingProfile1')
	ratingProfile2 = models.ForeignKey(Profile, related_name='ratingProfile2')
	rating = models.IntegerField(default=0)

class FacebookPairRating(models.Model):
	facebookPairRater = models.ForeignKey(Profile, related_name='facebookPairRater')
	friendFacebookID1 = models.CharField(max_length=255)
	friendFacebookID2 = models.CharField(max_length=255)
	rating = models.IntegerField(default=0)
