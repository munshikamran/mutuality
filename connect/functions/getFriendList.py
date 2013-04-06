from connect.models import Friendship,FacebookUser
from random import randint

# returns friendlist of user. args should take in a single value which is the limit of the returned querySet
# if you want the entire friendlist then don't specify args
# e.g. get entire friendlist: GetFriendList(profile)
# e.g. get 4 friends from friendlist: GetFriendList(profile, 4)
def GetFriendList(profile, *args):
    friendIDList = GetFriendIDs(profile)
    friendList = FacebookUser.objects.filter(facebookID__in=friendIDList)
    if len(args) > 0:
        limit = args[0]
        # truly random group of friends (may have performance issues)
        # return friendList.order_by('?')[:limit]
        # random offset group of friends
        offset = randint(0, max(0, friendList.count()-limit-1))
        return friendList[offset:offset + limit]
    return friendList


def GetFriendIDs(profile):
    friendListIDs = Friendship.objects.filter(user=profile).values_list('friend_id', flat=True)
    return friendListIDs

