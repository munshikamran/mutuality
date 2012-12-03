from connect.models import Profile,Friendship,FacebookUser

def GetFriendList(profile):
    friendIDList = GetFriendIDs(profile)
    friendList = FacebookUser.objects.filter(facebookID__in=friendIDList)
    return friendList


def GetFriendIDs(profile):
    friendships = list(Friendship.objects.filter(user=profile).values_list('friend'))
    friendIDList = []
    for friendship in friendships:
        friendIDList.append(friendship[0])
    return friendIDList

