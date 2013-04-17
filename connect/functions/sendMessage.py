from messages.models import Message
from connect.models import Profile
from connect.tasks.message_sent import message_sent

def SendMessage(profile,otherUserFacebookID,messageBody):
    try:
        sender = profile
        recipient = Profile.objects.get(facebookID=otherUserFacebookID)
        body = messageBody
        message = Message(sender=sender, recipient=recipient,body=body)
        message.save()
        message_sent(message)
        return True
    except:
        return False