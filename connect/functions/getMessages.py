from messages.models import Message
from datetime import datetime, timedelta
from django.db.models import Q


def GetRecentMessages(profile):
    now = datetime.now()
    pastDate = now - timedelta(weeks=4)
    return getMessagesSince(pastDate)

def GetMessageThreadWithOther(profile,otherProfile):
    q =  Q(sender_deleted_at__isnull=True) & (Q(sender_id=profile.user_id) & Q(recipient_id=profile.user_id)) | (Q(sender_id=otherProfile.user_id) & Q(recipient_id=profile.user_id))
    #order older messages first
    return Message.objects.filter(q).order_by('sent_at')

#private
def getMessagesSince(profile,pastDate):
    q = Q(sender_deleted_at__isnull=True) & (Q(sender_id=profile.user_id) | Q(recipient_id=profile.user_id)) & Q(sent_at__gte=pastDate)
    #order newer messages first
    return Message.objects.filter(q).order_by('sent_at').reverse()