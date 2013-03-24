from getMutualityUsers import GetNonFriendUsersInArea, GetNonFriendSingleUsersInArea
from getFriendsOfFriends import GetFriendsOfFriendsInArea, GetFriendsOfFriendsSingleInArea
from getViewedUsers import GetViewedUsers
from orderByNumberOfMutualFriends import OrderByNumberOfMutualFriends
from connect.models import FacebookUser
from connect.classes import MeetPeopleResponse

from common.enums import MEET_PEOPLE_FILTER

def GetMeetPeople(profile, filter):

    mutualityUsers = []
    friendsOfFriends = []
    if filter == MEET_PEOPLE_FILTER.FRIENDSHIP:
        mutualityUsers = GetNonFriendUsersInArea(profile)
        friendsOfFriends = GetFriendsOfFriendsInArea(profile)
    if filter == MEET_PEOPLE_FILTER.DATING:
        mutualityUsers = GetNonFriendSingleUsersInArea(profile)
        friendsOfFriends = GetFriendsOfFriendsSingleInArea(profile)
    facebookUserIDSet = set()
    mutualityUserIDSet = set()
    for person in mutualityUsers:
        mutualityUserIDSet.add(person.facebookID)
    for person in friendsOfFriends:
        facebookUserIDSet.add(person.facebookID)

    combinedUserIDSet = facebookUserIDSet.union(mutualityUserIDSet)
    #remove users who have already been seen
    viewedUsers = GetViewedUsers(profile, filter)
    viewedUserSet = set()
    for viewedUser in viewedUsers:
        viewedUserSet.add(viewedUser.facebookID)
    combinedUserIDSet = combinedUserIDSet.difference(viewedUserSet)

#    get users who user has not yet seen and order them by mutual friends
    freshUsers = FacebookUser.objects.filter(facebookID__in=list(combinedUserIDSet)).exclude(facebookID__in=viewedUsers)
    freshUsersOrdered = OrderByNumberOfMutualFriends(profile,list(freshUsers))
    # set a boolean, isMutualityUser, for determining if the person being shown is a user of mutuality
    setMutualityUsers(freshUsersOrdered, mutualityUserIDSet)
    setMutualityUsers(viewedUsers, mutualityUserIDSet)
    meetPeopleResponse = MeetPeopleResponse(freshUsersOrdered,viewedUsers)
    return meetPeopleResponse

# sets a boolean, isMutualityUser, for each object in facebookUsers. isMutualityUser=YES if user is a member of the site.
# note: this modifies the facebookUsers input.
def setMutualityUsers(facebookUsers, mutualityUserIDSet):
    for facebookUser in facebookUsers:
        facebookUser.isMutualityUser = facebookUser.facebookID in mutualityUserIDSet

