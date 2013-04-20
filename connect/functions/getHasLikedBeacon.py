from connect.models.beaconUserLike import BeaconUserLike


def hasLikedBeacon(myProfile, theirFbID):
    beaconLikes = BeaconUserLike.objects.filter(user=myProfile, beacon__user_id=theirFbID).exists()
    return beaconLikes
