from connect.models.beaconUserLike import BeaconUserLike
from connect.models.beacon import Beacon
from connect.models.profile import Profile

def LikeBeacon(profile, facebookID):
    try:
        otherProfile = Profile.objects.filter(facebookID=facebookID)
        beacon = Beacon.objects.filter(profile=otherProfile).latest()
        beaconUserLike = BeaconUserLike(profile=profile, beacon=beacon)
        beaconUserLike.save()
        return True
    except:
        return False

def GetBeaconLikeCount(beacon):
    BeaconUserLike.objects.filter(beacon=beacon).count()
