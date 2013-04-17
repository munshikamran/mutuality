from emails.tasks.email import send_user_joined_email, send_welcome_email, send_friend_joined_email
from emails.tasks.welcome_message import send_welcome_message


def user_joined(profile):
    send_user_joined_email.delay(profile)
    send_welcome_email.delay(profile)
    send_welcome_message.delay(profile)
       # excute this in the future so we know that we already have the user's friendlist in the db
    send_friend_joined_email.apply_async(args=[profile], countdown=60*10)
    return True