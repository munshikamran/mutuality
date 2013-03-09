from connect.models import Profile

# user data is a dictionary which can contain any of the following key value pairs
# 'name' : name of user
# 'birthdayString' : e.g. '12/30/1984'
# 'location' : <city>,<state> e.g. 'Seattle, Washington'
#  'relationship_status' : one of the values in common.enums.relationship_status.py
def UpdateProfile(profile,userData):
    profile.updateUsingFacebookDictionary(userData)
    profile.save()