from connect.models.beaconUserLike import BeaconUserLike
from connect.models.beacon import Beacon
from connect.models.profile import Profile

def LikeBeacon(profile, facebookID):
    try:
        otherProfile = Profile.objects.get(facebookID=facebookID)
        print otherProfile.name
        beacon = Beacon.objects.filter(user=otherProfile).latest('date_created')
        print beacon
        beaconUserLike, created = BeaconUserLike.objects.get_or_create(user=profile, beacon=beacon)
        if created:
            beaconUserLike.save()
        return True
    except:
        return False

def GetBeaconLikeCount(beacon):
    return BeaconUserLike.objects.filter(beacon=beacon).count()
