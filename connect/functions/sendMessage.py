from messages.models import Message

def SendMessageToOtherProfile(profile,otherProfile,messageBody):
    sender = profile.user
    recipient = otherProfile.user
    body = messageBody
    message = Message(sender = sender, recipient = recipient,body = body)
    message.save()