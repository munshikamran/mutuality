from connect.models.beaconUserLike import BeaconUserLike
from connect.models.beacon import Beacon

def hasLikedBeacon(myProfile, theirFbID):
    beacons = Beacon.objects.filter(user=theirFbID).latest('date_created').id
    beaconLikes = BeaconUserLike.objects.filter(user=myProfile, beacon_id=beacons).exists()
    return beaconLikes
