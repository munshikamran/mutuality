from django.conf.urls.defaults import *
from connect.views import *

urlpatterns = patterns('Mutuality.connect.views',
    url(r'^/?$', "index", name="index"),
    url(r'^profile/$', "profile", name="profile"),
    url(r'^profile/(\d+)/$', "profile", name="profile"),
    url(r'^makematches/?$', "makematches", name="makematches"),
    url(r'^fbinfo/?$', "fbinfo", name="fbinfo"),
    url(r'^register/$', register, name="register")
)


