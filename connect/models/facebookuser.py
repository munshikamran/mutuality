from django.db import models

from common.enums import RELATIONSHIP_STATUS
from common.enums import GENDER
import datetime

class FacebookUser( models.Model ):

	#id
	facebookID = models.CharField(max_length=255,primary_key=True)
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

	def __unicode__(self):
			return "%s  %s" % ( self.name, self.facebookID)

	@property
	def age(self):
		if self.birthdayDate:
			today = datetime.date.today()
			years = today.year - self.birthdayDate.year
			birthday = datetime.date(today.year, self.birthdayDate.month, self.birthdayDate.day)
			if today < birthday:
				years -= 1
			return years
		return None

	def updateUsingFacebookDictionary(self,fbDictionary):
		nameKey = 'name'
		if nameKey in fbDictionary.keys():
			self.name = fbDictionary[nameKey]
		# update gender
		genderKey = 'gender'
		if genderKey in fbDictionary.keys():
			gender = fbDictionary[genderKey]
			if gender == 'male' or gender == 'Male':
				self.gender = GENDER.MALE
			elif gender == 'female' or gender == 'Female':
				self.gender = GENDER.FEMALE

		# update age
		birthdayKey = 'birthday'
		if birthdayKey in fbDictionary.keys():
			bday = fbDictionary[birthdayKey].split('/')
			self.birthdayString = bday
			# birthday must include year for us to calculate age
			if len(bday)==3:
				self.birthdayDate = datetime.datetime(int(bday[2]),int(bday[0]),int(bday[1]))

		 # update relationship status
		relationshipStatusKey = 'relationship_status'
		if relationshipStatusKey in fbDictionary.keys():
			self.relationshipStatus = fbDictionary[relationshipStatusKey]

		# update location
		locationKey = 'location'
		if locationKey in fbDictionary.keys() and not (fbDictionary[locationKey]['name'] == None):
			self.location = fbDictionary[locationKey]['name']
			state = fbDictionary[locationKey]['name'].split(', ')[-1]
			self.state = state

		#the following are not stored in the database
		workKey = 'work'
		try:
#            this is a list of jobs. First element is most recent job (I think)
			self.employer = fbDictionary[workKey][0]["employer"]["name"]
		except:
			pass

		educationKey = 'education'
		try:
			educations = fbDictionary[educationKey]
			for education in educations:
				if education["type"] == 'College':
					self.college = education['school']['name']
		except:
			pass





