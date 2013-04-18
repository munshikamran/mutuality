from connect.models import PotentialMatch
from connect.models import PotentialMatchUpdate
from connect.models import PotentialBatch
from connect.functions.updatePotentialMatches import UpdatePotentialMatches
from connect.functions.getViewedUsers import GetAllViewedUsers
from datetime import datetime, timedelta
from common.enums import GENDER
import pytz
import settings


def CreatePotentialBatch(profile):
    if not PotentialMatch.objects.filter(profile=profile).exists():
        UpdatePotentialMatches(profile)
#     get potential matches for profile, remove users that have been seen
    batchSize = 20
    viewedUsers = GetAllViewedUsers(profile)
    userGender = profile.gender
    if not userGender:
        userGender = GENDER.MALE
    sameGenderPotentialMatches = PotentialMatch.objects.filter(profile=profile, facebookUser__gender__in=[userGender, None]).exclude(facebookUser__in=viewedUsers)
    sameGenderPotentialMatches = sameGenderPotentialMatches.order_by('-isMutualityConnection',
                                                                     '-numMutualFriends')[:batchSize/2]

    otherGender = GENDER.FEMALE
    if userGender == GENDER.FEMALE:
        otherGender = GENDER.MALE
    otherGenderPotentialMatches = PotentialMatch.objects.filter(profile=profile, facebookUser__gender=otherGender).exclude(facebookUser__in=viewedUsers)
    otherGenderPotentialMatches = otherGenderPotentialMatches.order_by('-isMutualityConnection',
                                                                 '-numMutualFriends')[:batchSize/2]

    potentialMatches = set(sameGenderPotentialMatches).union(set(otherGenderPotentialMatches))
    if len(potentialMatches) < 1:
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
    pacific = pytz.timezone('US/Pacific')
    currentDateTime = datetime.now(pacific)
    pastNoon = currentDateTime.hour >= 12
    referenceDate = currentDateTime
    if pastNoon:
        tomorrowDateTime = currentDateTime + timedelta(days=1)
        referenceDate = tomorrowDateTime
    year = referenceDate.year
    month = referenceDate.month
    day = referenceDate.day
    timeAtNoon = datetime(year, month, day, 12, 0, tzinfo=pacific)
    timezone = pytz.timezone(settings.TIME_ZONE)
    timezoneDateTime = timezone.normalize(timeAtNoon.astimezone(timezone))
    naiveDateTime = datetime(timezoneDateTime.year, timezoneDateTime.month, timezoneDateTime.day,
                             timezoneDateTime.hour, timezoneDateTime.minute)
    return naiveDateTime







