from django.conf.urls.defaults import *
from connect.views import *

urlpatterns = patterns('Mutuality.connect.views',
    url(r'^/?$', "index", name="index"),
    url(r'^api/', include( 'REST.urls' )),
    url(r'^profile/$', "profile", name="profile"),
    url(r'^profile/(\d+)/$', "profile", name="profile"),
    url(r'^makematches/?$', "makematches", name="makematches"),
    url(r'^meetpeople/?$', "meetpeople", name="meetpeople"),
    url(r'^fbinfo/?$', "fbinfo", name="fbinfo"),
    url(r'^register/$', register, name="register")
)


