from connect.classes import MeetPeopleResponse

from common.enums import MEET_PEOPLE_FILTER
from connect.functions.createPotentialBatch import CreatePotentialBatch
from connect.models import PotentialBatch
from connect.models import PotentialMatch
from datetime import datetime
from common.enums import RELATIONSHIP_STATUS


def GetMeetPeople(profile, filter):
    if not PotentialBatch.objects.filter(profile=profile, date_expiration__gt=datetime.now()).exists():
        CreatePotentialBatch(profile)
    batch = PotentialBatch.objects.filter(profile=profile).order_by('-date_created')[0]
    potentialMatches = PotentialMatch.objects.filter(potentialMatchBatch=batch).select_related('facebookUser')
    if filter == MEET_PEOPLE_FILTER.DATING:
        genderToExclude = profile.gender
        relationshipStatusesToExclude = [RELATIONSHIP_STATUS.RELATIONSHIP, RELATIONSHIP_STATUS.ENGAGED, RELATIONSHIP_STATUS.MARRIED]
        potentialMatches = potentialMatches.exclude(facebookUser__gender=genderToExclude).exclude(facebookUser__relationshipStatus__in=relationshipStatusesToExclude)
    # TODO filter out users who have been seen
    viewedUsers = []
    freshUsers = []
    for potentialMatch in potentialMatches:
        facebookUser = potentialMatch.facebookUser
        facebookUser.isMutualityUser = potentialMatch.isMutualityConnection
        freshUsers.append(facebookUser)
    meetPeopleResponse = MeetPeopleResponse(freshUsers, viewedUsers)
    return meetPeopleResponse

