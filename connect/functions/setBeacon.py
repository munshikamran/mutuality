from connect.models.beacon import Beacon
from connect.models.userViewed import UserViewed

def SetBeacon(profile, placeString, activityName):
    try:
        beacon = Beacon.objects.create(user=profile, place=placeString, activity=activityName)
        # delete all UserViewed objects with this user so she surfaces again in people's meet people results
        UserViewed.objects.filter(viewed_id=profile.facebookID).delete()
        return True
    except:
        return False
