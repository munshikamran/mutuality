from messages.models import Message
from connect.models import Profile
def SendMessage(profile,otherUserFacebookID,messageBody):
    sender = profile
    recipient = Profile.objects.get(facebookID=otherUserFacebookID)
    body = messageBody
    message = Message(sender = sender, recipient = recipient,body = body)
    message.save()