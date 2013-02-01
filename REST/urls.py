from django.conf.urls import patterns, url
from REST.views.get_profile import GetProfile
from REST.views.get_friend_list import GetFriendsList
from REST.views.get_match import GetMatch
from REST.views.update_friend_list import UpdateFriendListAPI
from REST.views.rate_match_thumbsup import RateMatchThumbsUpAPI
from REST.views.rate_match_thumbsdown import RateMatchThumbsDownAPI
from REST.views.get_friends_of_friends import GetFriendsOfFriendsList
from REST.views.get_meetpeople import GetMeetPeopleAPI
from REST.views.get_meetpeople_viewed import GetMeetPeopleViewedAPI
from REST.views.get_meetpeople_profile import GetMeetPeopleProfileAPI
from REST.views.get_mutualfriend_list import GetMutualFriendListAPI
from REST.views.get_favorites import GetFavoritesAPI
from REST.views.set_favorite import SetFavoriteAPI
from REST.views.set_user_viewed import SetUserViewedAPI

urlpatterns = patterns('REST.views',
    url(r'^getProfile/$', GetProfile.as_view()),
    url(r'^getFriendList/$', GetFriendsList.as_view()),
    url(r'^getNewMatch/$', GetMatch.as_view()),
    url(r'^updateFriendList/$', UpdateFriendListAPI.as_view()),
    url(r'^rateThumbsUp/$', RateMatchThumbsUpAPI.as_view()),
    url(r'^rateThumbsDown/$', RateMatchThumbsDownAPI.as_view()),
    url(r'^getFriendsOfFriendsList/$', GetFriendsOfFriendsList.as_view()),
    url(r'^getMeetPeople/$', GetMeetPeopleAPI.as_view()),
    url(r'^getMeetPeopleViewed/$', GetMeetPeopleViewedAPI.as_view()),
    url(r'^getMeetPeopleProfile/$', GetMeetPeopleProfileAPI.as_view()),
    url(r'^getMutualFriendList/$', GetMutualFriendListAPI.as_view()),
    url(r'^getFavoritesList/$', GetFavoritesAPI.as_view()),
    url(r'^setFavorite/$', SetFavoriteAPI.as_view()),
    url(r'^setUserViewed/$', SetUserViewedAPI.as_view()),
)
