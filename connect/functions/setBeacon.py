from connect.models.beacon import Beacon
from connect.models.beaconCategory import BeaconCategory

def SetBeacon(profile, placeString, categoryName):
    try:
        if BeaconCategory.objects.filter(name=categoryName).exists():
            category = BeaconCategory.objects.filter(name=categoryName)
            beacon = Beacon(profile=profile, place=placeString, category=category)
            beacon.save()
            return True
        else:
            return False
    except:
        return False