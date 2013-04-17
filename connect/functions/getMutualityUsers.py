from connect.models.profile import Profile
from connect.functions.getFriendList import GetFriendIDs
from common.enums import RELATIONSHIP_STATUS

def GetNonFriendUsersInArea(profile):
#    do not return users who are friends
    friendIDs = set(GetFriendIDs(profile))
    friendIDs.add(profile.facebookID)
    usersInArea = Profile.objects.filter(state=profile.state).exclude(facebookID__in=friendIDs)
    return usersInArea


def GetNonFriendSingleUsersInArea(profile):
    usersInArea = GetNonFriendUsersInArea(profile)
    genderToExclude = profile.gender
    relationshipStatusesToExclude = [RELATIONSHIP_STATUS.RELATIONSHIP,RELATIONSHIP_STATUS.ENGAGED,RELATIONSHIP_STATUS.RELATIONSHIP]
    return usersInArea.exclude(gender=genderToExclude).exclude(relationshipStatus__in=relationshipStatusesToExclude)
