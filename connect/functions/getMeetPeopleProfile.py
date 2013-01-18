from connect.models import FacebookUser
from connect.models import Friendship
from connect.classes import MeetPeopleProfile
from getProfileAuthToken import GetProfileAuthToken
import facebook

def GetMeetPeopleProfile(facebookUserID):
    try:
        facebookUser = FacebookUser.objects.get(facebookID = facebookUserID)
#        we need an auth token from a user who is friends with this person
        friendship = Friendship.objects.filter(friend=facebookUser)[0]
        someUserProfile = friendship.user
        graph = facebook.GraphAPI(GetProfileAuthToken(someUserProfile))
        fields = ['location','gender','birthday','relationship_status',"work","education"]
        kwargs = {"fields": fields}
        data=graph.get_object(facebookUserID,**kwargs)
        facebookUser.updateUsingFacebookDictionary(data)
        meetPeopleProfile = MeetPeopleProfile(facebookUser)
        return meetPeopleProfile
    except:
        print "error while getting meet people profile"

