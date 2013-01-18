from getMutualityUsers import GetNonFriendUsersInArea
from getFriendsOfFriends import GetFriendsOfFriendsInArea
from orderByNumberOfMutualFriends import OrderByNumberOfMutualFriends
from connect.models import FacebookUser

def GetMeetPeople(profile):
    mutualityUsers = GetNonFriendUsersInArea(profile)
    friendsOfFriends = GetFriendsOfFriendsInArea(profile)
    facebookUserIDSet = ()
    for person in mutualityUsers:
        facebookUserIDSet.add(person.facebookID)
    for person in friendsOfFriends:
        facebookUserIDSet.add(person.facebookID)
#    TODO remove users already seen
    people = FacebookUser.objects.filter(facebookID__in=list(facebookUserIDSet))
    orderedPeople = OrderByNumberOfMutualFriends(profile,people)
    return orderedPeople
