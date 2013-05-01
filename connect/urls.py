from django.conf.urls import *
from connect.views import *

urlpatterns = patterns('connect.views',
    url(r'^/?$', "index", name="index"),
    url(r'^api/', include( 'REST.urls' )),
    url(r'^makematches/?$', "makematches", name="makematches"),
    url(r'^meetpeople/?$', "meetpeople", name="meetpeople"),
    url(r'^messages/?$', "messages", name="messages"),
    url(r'^fbinfo/?$', "fbinfo", name="fbinfo"),
    url(r'^about/?$', "about", name="about"),
    url(r'^privacy/?$', "privacy", name="privacy"),
    url(r'^beacon/?$', "beacon", name="beacon"),
    url(r'^register/$', register, name="register"),
    url(r'^account/$', account, name="account"),
)

