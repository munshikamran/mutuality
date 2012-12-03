from getFriendList import GetFriendList

def GetMutualFriendList(profile1,profile2):
    friendList1 = GetFriendList(profile1)
    friendList2 = GetFriendList(profile2)
    friendListIntersection = friendList1.filter(pk__in=friendList2)
    return friendListIntersection

