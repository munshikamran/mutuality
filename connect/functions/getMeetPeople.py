from getMutualityUsers import GetNonFriendUsersInArea
from getFriendsOfFriends import GetFriendsOfFriendsInArea
from getViewedUsers import GetViewedUsers
from orderByNumberOfMutualFriends import OrderByNumberOfMutualFriends
from connect.models import FacebookUser
from connect.classes import MeetPeopleResponse

from common.enums import MEET_PEOPLE_FILTER

def GetMeetPeople(profile,filter):

    mutualityUsers = []
    friendsOfFriends = []
    if filter == MEET_PEOPLE_FILTER.FRIENDSHIP:
        mutualityUsers = GetNonFriendUsersInArea(profile)
        friendsOfFriends = GetFriendsOfFriendsInArea(profile)
    if filter == MEET_PEOPLE_FILTER.DATING:
        print "Dating filter not yet implemented"
    facebookUserIDSet = set()
    for person in mutualityUsers:
        facebookUserIDSet.add(person.facebookID)
    for person in friendsOfFriends:
        facebookUserIDSet.add(person.facebookID)

    #remove users who have already been seen
    viewedUsers = GetViewedUsers(profile,filter)
    viewedUserSet = set()
    for viewedUser in viewedUsers:
        viewedUserSet.add(viewedUser.facebookID)
    facebookUserIDSet = facebookUserIDSet.difference(viewedUserSet)

#    get users who user has not yet seen and order them by mutual friends
    freshUsers = FacebookUser.objects.filter(facebookID__in=list(facebookUserIDSet)).exclude(facebookID__in=viewedUsers)
    freshUsersOrdered = OrderByNumberOfMutualFriends(profile,list(freshUsers))
    meetPeopleResponse = MeetPeopleResponse(freshUsersOrdered,viewedUsers)
    return meetPeopleResponse
