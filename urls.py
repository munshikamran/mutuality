from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin 
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^', include('connect.urls')),
    url(r"^la_facebook/", include("la_facebook.urls")),
    (r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page':'/'}, name="logout"),
)

urlpatterns += patterns('',
	(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),	
)
