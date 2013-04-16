from django.db import models

class PageView(models.Model):
    user = models.ForeignKey('Profile', related_name="page_viewed_by")
    page_viewed = models.CharField(max_length=255)
    date_viewed = models.DateTimeField("Date Viewed", auto_now_add=True)

    class Meta:
        app_label = 'connect'