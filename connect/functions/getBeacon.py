from connect.models.beacon import Beacon

def GetBeacon(profile):
    try:
        if Beacon.objects.filter(profile=profile).exists():
            beacon = Beacon.objects.filter(profile=profile).latest('date_created')
            return beacon
        else:
            return []
    except:
        return False