from connect.models import *

def BeaconHasBeenSet(profile):
    return Beacon.objects.filter(user=profile).exists()