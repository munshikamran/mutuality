from connect.models import Friendship
from connect.models import FacebookUser

from getFriendList import GetFriendIDs

def GetFriendsOfFriends(profile):
    friendIDs = GetFriendIDs(profile)
    friendshipsOfFriends = list(Friendship.objects.filter(user__in=friendIDs).values_list('friend'))
    friendsOfFriendsIDs = []
    for friendship in friendshipsOfFriends:
        friendsOfFriendsIDs.append(friendship[0])

    uniqueFriends = set(friendsOfFriendsIDs).difference(set(friendIDs))
    friendsOfFriendsList = FacebookUser.objects.filter(facebookID__in=uniqueFriends)
    return friendsOfFriendsList

