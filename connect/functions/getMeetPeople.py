from getMutualityUsers import GetNonFriendUsersInArea, GetNonFriendSingleUsersInArea
from getFriendsOfFriends import GetFriendsOfFriendsInArea, GetFriendsOfFriendsSingleInArea
from getViewedUsers import GetViewedUsers, GetAllViewedUsers
from orderByNumberOfMutualFriends import OrderByNumberOfMutualFriends
from connect.models import FacebookUser
from connect.classes import MeetPeopleResponse

from common.enums import MEET_PEOPLE_FILTER
from connect.functions.createPotentialBatch import CreatePotentialBatch
from connect.models import PotentialBatch
from connect.models import PotentialMatch
from datetime import datetime
from common.enums import RELATIONSHIP_STATUS

# def GetMeetPeople(profile, filter):
#
#     mutualityUsers = []
#     friendsOfFriends = []
#     if filter == MEET_PEOPLE_FILTER.FRIENDSHIP:
#         mutualityUsers = GetNonFriendUsersInArea(profile)
#         friendsOfFriends = GetFriendsOfFriendsInArea(profile)
#     if filter == MEET_PEOPLE_FILTER.DATING:
#         mutualityUsers = GetNonFriendSingleUsersInArea(profile)
#         friendsOfFriends = GetFriendsOfFriendsSingleInArea(profile)
#     facebookUserIDSet = set()
#     mutualityUserIDSet = set()
#     for person in mutualityUsers:
#         mutualityUserIDSet.add(person.facebookID)
#     for person in friendsOfFriends:
#         facebookUserIDSet.add(person.facebookID)
#
#     combinedUserIDSet = facebookUserIDSet.union(mutualityUserIDSet)
#     #remove users who have already been seen
#     viewedUsers = GetViewedUsers(profile, filter)
#     viewedUserSet = set()
#     for viewedUser in viewedUsers:
#         viewedUserSet.add(viewedUser.facebookID)
#     combinedUserIDSet = combinedUserIDSet.difference(viewedUserSet)
#
# #    get users who user has not yet seen and order them by mutual friends
#     freshUsers = FacebookUser.objects.filter(facebookID__in=list(combinedUserIDSet)).exclude(facebookID__in=viewedUsers)
#     freshUsersOrdered = OrderByNumberOfMutualFriends(profile,list(freshUsers))
#     # set a boolean, isMutualityUser, for determining if the person being shown is a user of mutuality
#     setMutualityUsers(freshUsersOrdered, mutualityUserIDSet)
#     setMutualityUsers(viewedUsers, mutualityUserIDSet)
#     meetPeopleResponse = MeetPeopleResponse(freshUsersOrdered,viewedUsers)
#     return meetPeopleResponse
#
# # sets a boolean, isMutualityUser, for each object in facebookUsers. isMutualityUser=YES if user is a member of the site.
# # note: this modifies the facebookUsers input.
# def setMutualityUsers(facebookUsers, mutualityUserIDSet):
#     for facebookUser in facebookUsers:
#         facebookUser.isMutualityUser = facebookUser.facebookID in mutualityUserIDSet


def GetMeetPeople(profile, filter):
    if not PotentialBatch.objects.filter(profile=profile, date_expiration__gt=datetime.now()).exists():
        CreatePotentialBatch(profile)
    batch = PotentialBatch.objects.filter(profile=profile).order_by('-date_created')[0]
    potentialMatches = PotentialMatch.objects.filter(potentialMatchBatch=batch).select_related('facebookUser')
    if filter == MEET_PEOPLE_FILTER.DATING:
        genderToExclude = profile.gender
        relationshipStatusesToExclude = [RELATIONSHIP_STATUS.RELATIONSHIP,RELATIONSHIP_STATUS.ENGAGED,RELATIONSHIP_STATUS.MARRIED]
        potentialMatches = potentialMatches.exclude(facebookUser__gender=genderToExclude, facebookUser__relationshipStatus__in=relationshipStatusesToExclude)
    # TODO filter out users who have been seen
    viewedUsers = []
    freshUsers = []
    for potentialMatch in potentialMatches:
        facebookUser = potentialMatch.facebookUser
        facebookUser.isMutualityUser = potentialMatch.isMutualityConnection
        freshUsers.append(facebookUser)
    meetPeopleResponse = MeetPeopleResponse(freshUsers, viewedUsers)
    return meetPeopleResponse

