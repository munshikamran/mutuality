from connect.models.beacon import Beacon

def SetBeacon(profile, placeString, activityName):
    try:
        beacon = Beacon(user=profile, place=placeString, activity=activityName)
        beacon.save()
        return True
    except:
        return False

'''
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
                print cat.name
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
'''