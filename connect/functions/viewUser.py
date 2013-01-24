from connect.models import UserViewed,FacebookUser

def ViewUser(profile,facebookUserID,filter):
    try:
        facebookUser = FacebookUser.objects.get(facebookID=facebookUserID)
        userViewed, created = UserViewed.objects.get_or_create(user=profile, viewed=facebookUser, filter=filter)
        userViewed.save()
        return True
    except:
            print "error when creating viewed user"
