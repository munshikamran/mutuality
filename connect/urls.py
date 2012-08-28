from django.conf.urls.defaults import *

urlpatterns = patterns('Mutuality.connect.views',
    url(r'^/?$', "index", name="index"),
    url(r'^profile/?$', "profile", name="profile"),
    url(r'^dashboard/?$', "dashboard", name="dashboard"),
    url(r'^fbinfo/?$', "fbinfo", name="fbinfo")
)
