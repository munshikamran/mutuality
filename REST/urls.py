from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from REST.views import *

urlpatterns = patterns('Mutuality.REST.views',
    url(r'^profiles/get', 'get_profile'),
    url(r'^friends/list', 'friends_list'),
    url(r'^friends/list/male', 'friends_list_male'),
    url(r'^friends/list/female', 'friends_list_female'),
    url(r'^/api/getProfile', ProfileDetail.as_view())
)

urlpatterns = format_suffix_patterns(urlpatterns)
