from messages.models import Message
from emails.tasks import send_new_message_email


def message_sent(message):
    founder_ids = ['1240230066', '3900450', '1065870234']
    if message.sender.facebookID in founder_ids:
        return
    send_new_message_email.delay(message)