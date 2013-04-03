from connect.models import PotentialMatch
from connect.models import PotentialMatchUpdate
from connect.models import PotentialBatch
from connect.functions.updatePotentialMatches import UpdatePotentialMatches
from connect.functions import GetAllViewedUsers
from datetime import datetime, timedelta


def CreatePotentialBatch(profile):
    if not PotentialMatch.objects.filter(profile=profile).exists():
        UpdatePotentialMatches(profile)
#     get potential matches for profile, remove users that have been seen
    viewedUsers = GetAllViewedUsers(profile)
    potentialMatches = PotentialMatch.objects.filter(profile=profile).exclude(facebookUser__in=viewedUsers)
    potentialMatches = potentialMatches.order_by('-isMutualityConnection', '-numMutualFriends')
    if potentialMatches.count() < 1:
        print "no matches available"
        return None

    expirationDate = datetime.now() + timedelta(days=1)

    batchSize = 20
    potentialBatch = PotentialBatch.objects.create(profile=profile, date_expiration=expirationDate)
    potentialBatch.save()
    for i in range(min(potentialMatches.count(), batchSize)):
        potentialMatch = potentialMatches[i]
        potentialMatch.potentialMatchBatch = potentialBatch
        potentialMatch.save()
    return potentialBatch




