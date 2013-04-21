from connect.models.profile import Profile
from connect.models.potentialBatch import PotentialBatch
from connect.models.potentialMatch import PotentialMatch
# user data is a dictionary which can contain any of the following key value pairs
# 'name' : name of user
# 'birthdayString' : e.g. '12/30/1984'
# 'location' : <city>,<state> e.g. 'Seattle, Washington'
#  'relationship_status' : one of the values in common.enums.relationship_status.py
def UpdateProfile(profile, userData):
    currentState = profile.state
    profile.updateUsingFacebookDictionary(userData)
    profile.save()
    newState = profile.state
    # if the user has changed location, we must dump their current matches and get them new ones
    if not currentState == newState:
        PotentialBatch.objects.filter(profile=profile).delete()
        PotentialMatch.objects.filter(profile=profile).delete()