from connect.models import UserViewed


def GetViewedUsers(profile,meetPeopleFilter):
#    order by most recently viewed first
    try:
        userViews = UserViewed.objects.filter(user=profile).filter(filter=meetPeopleFilter).order_by('date_last_viewed').reverse()
        userViews = userViews.select_related("viewed")
        viewedUsers = []
        for userView in userViews:
            viewedUsers.append(userView.viewed)
        return viewedUsers
    except:
        print "error when fetching viewed users"
        return False


def GetAllViewedUsers(profile):
    # userViews = UserViewed.objects.filter(user=profile).distinct('viewed').select_related('viewed')
    userViews = UserViewed.objects.filter(user=profile).select_related('viewed')
    viewedUsers = []
    for userView in userViews:
        viewedUsers.append(userView.viewed)
    return viewedUsers
