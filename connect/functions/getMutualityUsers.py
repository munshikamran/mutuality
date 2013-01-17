from connect.models import Profile
from connect.functions import GetFriendIDs
def GetNonFriendUsersInArea(profile):
#    do not return users who are friends
    friendIDs = GetFriendIDs(profile)
    usersInArea = Profile.objects.filter(state=profile.state).exclude(facebookID__in=friendIDs+[profile.facebookID])
    return usersInArea


def GetNonFriendSingleUsers(profile):
    return []