from connect.classes import MeetPeopleResponse
from common.enums import MEET_PEOPLE_FILTER
from connect.functions.createPotentialBatch import CreatePotentialBatch
from connect.models import PotentialBatch
from connect.models import PotentialMatch
from connect.models.friendship import Friendship
from connect.models.userViewed import UserViewed
from connect.models.userFavorite import UserFavorite
from connect.models.profile import Profile
from datetime import datetime
from common.enums import RELATIONSHIP_STATUS


def GetMeetPeople(profile, meetPeopleFilter):
    # check if the users friend list has been uploaded
    if not Friendship.objects.filter(user=profile).exists():
        # the user has no friends or UpdateFriendList hasn't been called
        return MeetPeopleResponse([], MeetPeopleResponse.NO_FRIENDS_MESSAGE)

    facebookUsers = []
    if meetPeopleFilter == MEET_PEOPLE_FILTER.FRIENDSHIP or meetPeopleFilter == MEET_PEOPLE_FILTER.DATING:
        facebookUsers = getPotentialMatches(profile, meetPeopleFilter)
        if len(facebookUsers) < 1:
            return MeetPeopleResponse([], MeetPeopleResponse.SEEN_ALL_MATCHES_MESSAGE)
    elif meetPeopleFilter == MEET_PEOPLE_FILTER.VIEWED:
        facebookUsers = getViewedPeopleOrdered(profile)
    elif meetPeopleFilter == MEET_PEOPLE_FILTER.FAVORITES:
        facebookUsers = getFavorites(profile)

    facebookUsers = markFavorited(profile, facebookUsers)
    facebookUsers = markMutualityUsers(facebookUsers)
    meetPeopleResponse = MeetPeopleResponse(facebookUsers, MeetPeopleResponse.SUCCESS_MESSAGE)
    return meetPeopleResponse


def getPotentialMatches(profile, meetPeopleFilter):
    if not PotentialBatch.objects.filter(profile=profile, date_expiration__gt=datetime.now()).exists():
        CreatePotentialBatch(profile)
    batch = None
    potentialBatches = PotentialBatch.objects.filter(profile=profile).order_by('-date_created')
    if potentialBatches.exists():
        batch = potentialBatches[0]
    potentialMatches = PotentialMatch.objects.filter(potentialMatchBatch=batch).select_related('facebookUser')

    if meetPeopleFilter == MEET_PEOPLE_FILTER.DATING:
        genderToExclude = profile.gender
        relationshipStatusesToExclude = [RELATIONSHIP_STATUS.RELATIONSHIP, RELATIONSHIP_STATUS.ENGAGED,
                                         RELATIONSHIP_STATUS.MARRIED]
        potentialMatches = potentialMatches.exclude(facebookUser__gender=genderToExclude).exclude(
            facebookUser__relationshipStatus__in=relationshipStatusesToExclude)
    facebookUsers = []
    for potentialMatch in potentialMatches:
        facebookUsers.append(potentialMatch.facebookUser)
    return facebookUsers


def getViewedPeopleOrdered(profile):
    viewedUsers = UserViewed.objects.filter(user=profile).order_by('-date_last_viewed').select_related('viewed')
    facebookUsers = []
    for viewedUser in viewedUsers:
        facebookUsers.append(viewedUser.viewed)
    return facebookUsers


def getFavorites(profile):
    favorites = UserFavorite.objects.filter(user=profile).select_related('favorite')
    facebookUsers = []
    for favorite in favorites:
        facebookUsers.append(favorite.favorite)
    return facebookUsers

def markMutualityUsers(facebookUsers):
    facebookIDs = set()
    for facebookUser in facebookUsers:
        facebookIDs.add(facebookUser.facebookID)
    mutualityProfileIDs = set(Profile.objects.filter(facebookID__in=facebookIDs).values_list('facebookID', flat=True))
    for facebookUser in facebookUsers:
        facebookUser.isMutualityUser = facebookUser.facebookID in mutualityProfileIDs
    return facebookUsers


def markFavorited(profile, facebookUsers):
    favoriteIDs = set(UserFavorite.objects.filter(user=profile).values_list('favorite_id', flat=True))
    for facebookUser in facebookUsers:
        facebookUser.isFavorite = facebookUser.facebookID in favoriteIDs
    return facebookUsers



