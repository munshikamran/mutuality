from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('Mutuality.connect.views',
    url(r'^/?$', "index", name="index"),
    url(r'^profile/$', "profile", name="profile"),
    url(r'^profile/(\d+)/$', "profile", name="profile"),
    url(r'^makematches/?$', "makematches", name="makematches"),
    url(r'^fbinfo/?$', "fbinfo", name="fbinfo"),
    url(r'^spinSlotMachine$', spinSlotMachine, name="spinSlotMachine"),
    url(r'^submitRating$', submitRating, name="submitRating"),
    url(r'^register/$', register, name="register"),
    url(r'^profiles/get', 'get_profile'),
    url(r'^friends/list', 'friends_list'),
    url(r'^friends/list/male', 'friends_list_male'),
    url(r'^friends/list/female', 'friends_list_female'),

)
