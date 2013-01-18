from connect.models import UserViewed,FacebookUser

def ViewUser(profile,facebookUserID):
    try:
        facebookUser = FacebookUser.objects.get(facebookID=facebookUserID)
        print facebookUser
        userViewed, created = UserViewed.objects.get_or_create(user=profile, viewed=facebookUser)
        userViewed.save()
        return True
    except:
            print "error when creating viewed user"
