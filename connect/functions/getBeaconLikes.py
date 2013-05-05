from connect.models.beaconUserLike import BeaconUserLike


def GetBeaconLikes(beacon):
    beaconUserLikes = BeaconUserLike.objects.filter(beacon=beacon).select_related('user')
    users = []
    for beaconUserLike in beaconUserLikes:
        users.append(beaconUserLike.user)
    return users
