#!/usr/bin/env python
#!/usr/bin/env python

import os, sys

sys.path.insert(0, "/var/Mutuality/")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
