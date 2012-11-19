from connect.models import Profile,Friendship

def GetFriendList(profile):
    friendships = Friendship.objects.filter(user=profile)
    return friendships

