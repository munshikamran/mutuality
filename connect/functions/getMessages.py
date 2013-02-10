from messages.models import Message
from datetime import datetime, timedelta
from django.db.models import Q

# Thread preview functions return an array of Message objects. See messages.models for a full description of message
# objects. For quick reference message.sender and message.recipient are Profile objects. Thus message.sender.facebookID
# gives the facebook id of the sender. Message objects also include subject, body, and sent_at fields.
def GetAllThreadPreviews(profile):
    pastDate = datetime.min
    return GetThreadPreviewsSince(profile,pastDate)

def GetThreadPreviewsSince(profile,pastDate):
    messages = getMessagesSince(profile,pastDate)
    threadPreviews = []
    otherUsers = []
    for message in messages:
        otherUser = message.sender
        if otherUser == profile:
            otherUser = message.recipient
        if not otherUser.facebookID in otherUsers:
            otherUsers.append(otherUser.facebookID)
            threadPreviews.append(message)
    return threadPreviews


def GetMessageThreadWithOther(profile,otherProfile):
    q =  Q(sender_deleted_at__isnull=True) & (Q(sender=profile) & Q(recipient=otherProfile)) | (Q(sender=otherProfile) & Q(recipient=profile))
    #order older messages first
    return Message.objects.filter(q).order_by('sent_at')

#private
def getMessagesSince(profile,pastDate):
    q = Q(sender_deleted_at__isnull=True) & (Q(sender=profile) | Q(recipient=profile)) & Q(sent_at__gte=pastDate)
    #order newer messages first
    return Message.objects.filter(q).order_by('sent_at').reverse()