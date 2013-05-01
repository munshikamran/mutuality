from connect.models.beaconUserLike import BeaconUserLike
from connect.models.beacon import Beacon
from connect.models.profile import Profile

def LikeBeacon(token, facebookID):
    try:
        otherProfile = Profile.objects.get(facebookID=facebookID)
        profile = Profile.objects.get(facebookID=token)
        beacon = Beacon.objects.filter(user=otherProfile).latest('date_created')
        beaconUserLike, created = BeaconUserLike.objects.get_or_create(user=profile, beacon=beacon)
        if created:
            beaconUserLike.save()
        return True
    except:
        return False

def GetBeaconLikeCount(beacon):
    return BeaconUserLike.objects.filter(beacon=beacon).count()
