from django.conf.urls import patterns, url
from REST.views.get_profile import GetProfile
from REST.views.get_friend_list import GetFriendsList
from REST.views.get_match import GetMatch
from REST.views.update_friend_list import UpdateFriendListAPI
from REST.views.rate_match_thumbsup import RateMatchThumbsUpAPI

urlpatterns = patterns('REST.views',
    url(r'^getProfile/$', GetProfile.as_view()),
    url(r'^getFriendList/$', GetFriendsList.as_view()),
    url(r'^getNewMatch/$', GetMatch.as_view()),
    url(r'^updateFriendList/$', UpdateFriendListAPI.as_view()),
    url(r'^rateThumbsUp/$', RateMatchThumbsUpAPI.as_view())
)
