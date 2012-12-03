from connect.models import FacebookUser
from connect.models import FacebookUserMatch
from connect.models import FacebookUserMatchRating
from django.db.models import Q

def RateThumbsUp(profile,facebookUserID1,facebookUserID2):
    try:
        facebookUser1 = FacebookUser.objects.get(facebookID = facebookUserID1)
        facebookUser2 = FacebookUser.objects.get(facebookID = facebookUserID2)
        match = getOrCreateMatchWithUsers(profile,facebookUser1,facebookUser2)
        newRating, created = FacebookUserMatchRating.objects.get_or_create(match = match)
        newRating.thumbsUp = True
        newRating.save()
        return True
    except:
        return False


def getOrCreateMatchWithUsers(profile,facebookUser1,facebookUser2):
    q =  (Q(facebookUser1 = facebookUser1) & Q(facebookUser2=facebookUser2)) | (Q(facebookUser1 = facebookUser2) & Q(facebookUser2=facebookUser1))
    matches = FacebookUserMatch.objects.filter(q)
    if matches.exists():
        return matches[0]
    else:
        match = FacebookUserMatch(profile=profile,facebookUser1=facebookUser1,facebookUser2=facebookUser2)
        match.save()
        return match