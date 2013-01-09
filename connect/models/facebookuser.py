from django.db import models
from datetime import datetime

from common.enums import RELATIONSHIP_STATUS
from common.enums import GENDER

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

    def updateUsingFacebookDictionary(self,fbDictionary):
        nameKey = 'name'
        if nameKey in fbDictionary.keys():
            self.name = fbDictionary[nameKey].encode('unicode_escape')
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

         # update relationship status
        relationshipStatusKey = 'relationship_status'
        if relationshipStatusKey in fbDictionary.keys():
            self.relationshipStatus = fbDictionary[relationshipStatusKey]

    	# update location
    	locationKey = 'location'
    	if locationKey in fbDictionary.keys() and not (fbDictionary[locationKey]['name'] == None):
            print fbDictionary[locationKey]['name']
            self.location = fbDictionary[locationKey]['name'].encode('unicode_escape')
            state = fbDictionary[locationKey]['name'].split(', ')[-1]
            self.state = state
        self.save()



