from connect.models import PotentialMatch
from connect.models import PotentialMatchUpdate
from connect.models import PotentialBatch
from connect.functions.updatePotentialMatches import UpdatePotentialMatches
from connect.functions import GetAllViewedUsers
from datetime import datetime, timedelta
import pytz


def CreatePotentialBatch(profile):
    if not PotentialMatch.objects.filter(profile=profile).exists():
        UpdatePotentialMatches(profile)
#     get potential matches for profile, remove users that have been seen
    batchSize = 20
    viewedUsers = GetAllViewedUsers(profile)
    potentialMatches = PotentialMatch.objects.filter(profile=profile).exclude(facebookUser__in=viewedUsers)
    potentialMatches = potentialMatches.order_by('-isMutualityConnection', '-numMutualFriends')[:batchSize]
    if potentialMatches.count() < 1:
        print "no matches available"
        return None
    # weird problem with duplicates when QuerySet with order_by is allowed to evaluate lazily.
    # casting to list avoids this issue
    potentialMatches = list(potentialMatches)
    expirationDate = getTimeAtNoon()

    potentialBatch = PotentialBatch.objects.create(profile=profile, date_expiration=expirationDate)
    potentialBatch.save()
    for i in range(min(len(potentialMatches), batchSize)):
        potentialMatch = potentialMatches[i]
        potentialMatch.potentialMatchBatch = potentialBatch
        potentialMatch.save()
    return potentialBatch


def getTimeAtNoon():
    timezone = pytz.timezone('US/Pacific')
    currentDateTime = datetime.now(timezone)
    pastNoon = currentDateTime.hour >= 12
    referenceDate = currentDateTime
    if pastNoon:
        tomorrowDateTime = currentDateTime + timedelta(days=1)
        referenceDate = tomorrowDateTime
    year = referenceDate.year
    month = referenceDate.month
    day = referenceDate.day
    timeAtNoon = datetime(year, month, day, 12, 0, tzinfo=timezone)
    utc = pytz.timezone('UTC')
    utcDateTime = utc.normalize(timeAtNoon.astimezone(utc))
    naiveDateTime = datetime(utcDateTime.year, utcDateTime.month, utcDateTime.day,
                             utcDateTime.hour, utcDateTime.minute)
    return naiveDateTime







