from django.conf.urls import patterns, url
from REST.views.get_profile import GetProfile
from REST.views.get_friend_list import GetFriendsList
from REST.views.get_match import GetMatch
from REST.views.update_friend_list import UpdateFriendListAPI
from REST.views.update_friend_list_called import UpdateFriendListCalledAPI
from REST.views.rate_match_thumbsup import RateMatchThumbsUpAPI
from REST.views.rate_match_thumbsdown import RateMatchThumbsDownAPI
from REST.views.get_friends_of_friends import GetFriendsOfFriendsList
from REST.views.get_favorites import GetFavoritesAPI
from REST.views.set_favorite import SetFavoriteAPI
from REST.views.get_meetpeople import GetMeetPeopleAPI
from REST.views.get_meetpeople_profile import GetMeetPeopleProfileAPI
from REST.views.get_mutualfriend_list import GetMutualFriendListAPI
from REST.views.set_user_viewed import SetUserViewedAPI
from REST.views.get_thread_previews import GetThreadPreviewsAPI
from REST.views.get_newmessage_count import GetNewMessageCountAPI
from REST.views.get_message_with_other import GetMessageThreadWithOtherAPI
from REST.views.send_message import SendMessageAPI
from REST.views.remove_favorite import RemoveFavoriteAPI
from REST.views.set_profile import SetProfileAPI
from REST.views.mobile_auth import MobileAuthAPI
from REST.views.get_beacon import GetBeaconAPI
from REST.views.set_beacon import SetBeaconAPI
from REST.views.like_beacon import LikeBeaconAPI
from REST.views.get_beacon_like_count import GetBeaconLikeCountAPI
from REST.views.get_hasLikedBeacon import GetHasLikedBeaconAPI


urlpatterns = patterns('REST.views',
    url(r'^getProfile/$', GetProfile.as_view()),
    url(r'^getFriendList/$', GetFriendsList.as_view()),
    url(r'^getNewMatch/$', GetMatch.as_view()),
    url(r'^updateFriendList/$', UpdateFriendListAPI.as_view()),
    url(r'^updateFriendListCalled/$', UpdateFriendListCalledAPI.as_view()),
    url(r'^rateThumbsUp/$', RateMatchThumbsUpAPI.as_view()),
    url(r'^rateThumbsDown/$', RateMatchThumbsDownAPI.as_view()),
    url(r'^getFriendsOfFriendsList/$', GetFriendsOfFriendsList.as_view()),
    url(r'^getMutualFriendList/$', GetMutualFriendListAPI.as_view()),
    url(r'^getFavoritesList/$', GetFavoritesAPI.as_view()),
    url(r'^setFavorite/$', SetFavoriteAPI.as_view()),
    url(r'^getMeetPeople/$', GetMeetPeopleAPI.as_view()),
    url(r'^getMeetPeopleProfile/$', GetMeetPeopleProfileAPI.as_view()),
    url(r'^setUserViewed/$', SetUserViewedAPI.as_view()),
    url(r'^getThreadPreviews/$', GetThreadPreviewsAPI.as_view()),
    url(r'^getNewMessageCount/$', GetNewMessageCountAPI.as_view()),
    url(r'^getMessagesWithOther/$', GetMessageThreadWithOtherAPI.as_view()),
    url(r'^sendMessage/$', SendMessageAPI.as_view()),
    url(r'^removeFavorite/$', RemoveFavoriteAPI.as_view()),
    url(r'^setProfile/$', SetProfileAPI.as_view()),
    url(r'^mobileauth/$', MobileAuthAPI.as_view()),
    url(r'^getBeacon/$', GetBeaconAPI.as_view()),
    url(r'^setBeacon/$', SetBeaconAPI.as_view()),
    url(r'^likeBeacon/$', LikeBeaconAPI.as_view()),
    url(r'^getBeaconLikeCount/$', GetBeaconLikeCountAPI.as_view()),
    url(r'^getHasLikedBeacon/$', GetHasLikedBeaconAPI.as_view())
)
