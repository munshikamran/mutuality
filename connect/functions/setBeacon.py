from connect.models.beacon import Beacon
from connect.models.beaconActivity import BeaconActivity
from connect.models.beaconCategory import BeaconCategory

def SetBeacon(profile, placeString, activityName, **kwargs):
    try:
        if BeaconActivity.objects.filter(name=activityName).exists():
            # An activity with this name exists already
            activity = BeaconActivity.objects.get(name=activityName)
            beacon = Beacon(user=profile, place=placeString, activity=activity)
            beacon.save()
        else:
            # We should create a custom activity then
            if BeaconCategory.objects.filter(name=kwargs['categoryName']).exists():
                cat = BeaconCategory.objects.get(name=kwargs['categoryName'])
                activity = BeaconActivity(name=activityName, category=cat)
                activity.save()
                # and then use it for this beacon
                beacon = Beacon(user=profile, place=placeString, activity=activity)
                beacon.save()
            else:
                return False
        return True
    except:
        return False