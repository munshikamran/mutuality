from messages.models import Message
from connect.models import Profile
from datetime import datetime
from django.db.models import Q


def GetNewMessageCount(profile):
    receivedMessageCount = Message.objects.filter(recipient=profile).filter(read_at__isnull=True).count()
    return receivedMessageCount

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


def GetMessageThreadWithOther(profile,otherUserFacebookID):
    otherProfile = Profile.objects.get(facebookID=otherUserFacebookID)
    q =  Q(sender_deleted_at__isnull=True) & (Q(sender=profile) & Q(recipient=otherProfile)) | (Q(sender=otherProfile) & Q(recipient=profile))
    #order older messages first
    messages = Message.objects.filter(q).order_by('sent_at').select_related('sender','recipient')
    # once these messages are returned we mark them as read
    now = datetime.now()
    for message in messages:
        if not message.read_at and profile == message.recipient:
            message.read_at = now
            message.save()
    return Message.objects.filter(q).order_by('sent_at')

#private
def getMessagesSince(profile,pastDate):
    q = Q(sender_deleted_at__isnull=True) & (Q(sender=profile) | Q(recipient=profile)) & Q(sent_at__gte=pastDate)
    #order newer messages first
    return Message.objects.filter(q).order_by('sent_at').reverse().select_related('sender','recipient')