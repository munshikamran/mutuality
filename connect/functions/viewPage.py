from connect.models import PageView
from common.enums.site_pages import SITE_PAGES

# called when a page is viewed by a user. Possible values for sitePage are in common.enums.site_pages.py
# example usage: ViewPage(profile, SITE_PAGES.MEET_PEOPLE)
def ViewPage(profile, sitePage):
    PageView.objects.create(user=profile, page_viewed=sitePage)

# returns False if a page has never been viewed by a user before, True otherwise.
# Note: you will likely want to call this BEFORE ViewPage.
def PageHasBeenViewed(profile, sitePage):
    hasBeenViewed = PageView.objects.filter(user=profile, page_viewed=sitePage).exists()
    return hasBeenViewed