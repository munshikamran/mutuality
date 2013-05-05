import settings
import sendgrid
from celery import task
from celery.task import periodic_task
from django.core.mail import send_mail
from connect.functions.getFriendList import GetFriendIDs
from connect.functions.getMutualFriendList import GetMutualFriendListWithFacebookUserID
from connect.models.profile import Profile
from connect.models.facebookuser import FacebookUser
from connect.models.potentialMatch import PotentialMatch
from connect.functions.getMeetPeople import GetMeetPeople
from emails.models import Email
from datetime import datetime, timedelta


def send_email_to_all_users(subject, text, html, from_address):
    for profile in Profile.objects.all():
        try:
            message = sendgrid.Message(from_address, subject, text, html)
            message.add_to(profile.user.email, profile.name)
            send_message(message, profile.user, Email.DEFAULT)
        except:
            print 'something went wrong when sending an email to ' + profile.name

@task
def send_user_joined_email(profile):
    recipients = ['jeffreymames@gmail.com', 'jazjit.singh@gmail.com', 'kamran.munshi@gmail.com']
    subject = 'A New User Joined Mutuality!'
    message = '{0} joined Mutuality'.format(profile.name)
    return send_mail(subject, message, 'info@mutuality.com', recipients, fail_silently=False)

@periodic_task(run_every=timedelta(seconds=10))
def send_i_joined_email():
    print 'sending email'
    profile = Profile.objects.get(name="Jeff Ames")
    send_user_joined_email(profile)

@task
def send_welcome_email(profile):
    from_address = 'info@mymutuality.com'
    to_address = profile.user.email
    to_name = profile.name
    message = create_welcome_message(from_address, to_address, to_name)
    send_message(message, profile.user, Email.WELCOME)

@task
def send_friend_joined_email(joined_user_profile):
    from_address = 'info@mymutuality.com'
    friendIDs = GetFriendIDs(joined_user_profile)
    friendsOnMutuality = Profile.objects.filter(facebookID__in=friendIDs)
    for profile in friendsOnMutuality:
        try:
            to_address = profile.user.email
            to_name = profile.name
            friendName = joined_user_profile.name
            friendFacebookID = joined_user_profile.facebookID
            friendsFriends = GetFriendIDs(profile)
            numberOfNewFriends = FacebookUser.objects.filter(facebookID__in=(set(friendIDs).difference(friendsFriends)), state=profile.state).count()
            totalNumberOfFriends = len(friendsFriends)
            currentNumberOfFoF = PotentialMatch.objects.filter(profile=profile).count()
            city = profile.location.split(',')[0]
            message = create_friend_joined_message(from_address, to_address, to_name, friendName, friendFacebookID, numberOfNewFriends, totalNumberOfFriends, currentNumberOfFoF, city)
            send_message(message, profile.user, Email.FRIEND_JOINED)
        except:
            print "something went wrong when sending email to {0}'s friend {1}".format(joined_user_profile.name, profile.name)


@task
def send_new_message_email(message):
    from_address = 'info@mymutuality.com'
    sender_name = message.sender.name
    mutualFriendList = GetMutualFriendListWithFacebookUserID(message.recipient, message.sender.facebookID)
    mutual_friend_count = len(mutualFriendList)
    mutual_friend_name = mutualFriendList[0].name
    to_address = message.recipient.user.email
    to_name = message.recipient.name
    email = create_new_message_message(from_address, to_address, to_name, sender_name,
                                       mutual_friend_count, mutual_friend_name)
    send_message(email, message.recipient.user, Email.NEW_MESSAGE)


def send_all_inactive_emails():
    tasks = []
    past = datetime.now() - timedelta(days=5)
    inactive_profiles = Profile.objects.filter(user__last_login__lte=past)
    tasks = []
    for profile in inactive_profiles:
        try:
            #     check if we have already sent email
            already_sent = Email.objects.filter(user=profile.user, email_type=Email.USER_INACTIVE, sent_at__gte=past).exists()
            if not already_sent:
                task = send_inactive_email.delay(profile)
                tasks.append(task)
        except:
            print 'something went wrong when sending inactive email to {0}'.format(profile.name)
    return tasks



@task
def send_inactive_email(profile):
    from common.enums.meetPeopleFilters import MEET_PEOPLE_FILTER
    from_address = 'info@mymutuality.com'
    to_address = profile.user.email
    to_name = profile.name
    new_friend = GetMeetPeople(profile, MEET_PEOPLE_FILTER.FRIENDSHIP).potentialMatches[0]
    new_friend_name = new_friend.name
    new_friend_facebookID = new_friend.facebookID
    mutual_friend_list = GetMutualFriendListWithFacebookUserID(profile, new_friend.facebookID)
    mutual_friend_count = len(mutual_friend_list)
    mutual_friend_name = mutual_friend_list[0].name
    email = create_inactive_message(from_address, to_address, to_name, new_friend_name,
                                    new_friend_facebookID, mutual_friend_count, mutual_friend_name)
    send_message(email, profile.user, Email.USER_INACTIVE)


def send_message(message, to_user, email_type):
    email = Email(user=to_user, subject=message.subject, text_body=message.text,
                  html_body=message.html, to_address=message.to[0], from_address=message.from_address,
                  email_type=email_type)
    email.save()
    s = sendgrid.Sendgrid(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, secure=True)
    s.smtp.send(message)


# HTML messages
def create_welcome_message(from_address, to_address, to_name):
    html = '''<html><title>Welcome to Mutuality</title><body style = "margin:0px 0px 0px 0px;padding: 0px 0px 0px 0px; font-family: Tahoma, Geneva, sans-serif;"><!-- Start Main Table --><table width = "100%" height="100%" cellpadding = "0" style="padding:20px 0px 20px 0px" bgcolor="#FFFFFF"><table align="center"><tr><td width="460px" height="50px"><!-- Start Header --><table width="460px" cellpadding="0px" cellspacing="0" bgcolor="#6ba4c5" style = "color:#FFFFFF; font-weight: regular; padding: 16px 0px 16px 14px; font-family: Tahoma, Geneva, sans-serif;"><tr><td><a href='http://www.mymutuality.com?src=email_welcome'><img src="http://www.mymutuality.com/images/bigLogo.jpg" width="130" height="35" alt="Logo" border="0"></a></td></tr></table></td></tr></table><!-- End Header --><!-- Start Next Section --><table align="center"><tr><td width="460px" height="100px"><table cellpadding="0" cellspacing="0" width="460px" bgcolor="FFFFFF"><tr><td width="200" height="100" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 10px 10px 0px 15px; font-size: 16px; color:#000; font-weight:regular"><span style="font-size:34px; color:#989898; font-weight=regular">Welcome!</span><br><br>Creep.com? Never again.<br><br><br></td><td width="260" height="100" cellspacing="0" bgcolor="FFFFFF"><img src="http://www.mymutuality.com/images/carousel.jpg" alt="Image blocked" border="0"></td></tr></table></td></tr><tr><td><table cellpadding="0" cellspacing="0" width="460" bgcolor="FFFFFF"><tr><td width="200" height="120" bgcolor="FFFFFF" style="padding: 0px 0px 0px 20px"><img src="http://www.mymutuality.com/images/connected.jpg" alt="Image blocked" border="0"></td><td width="260" align="center" height="120" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 18px; color:#000; font-weight:regular">You are connected<br>to everyone you see.</td></tr></table></td></tr><tr><td><table cellpadding="0" cellspacing="0" width="460" bgcolor="FFFFFF"><tr><td width="260" align="center" height="120" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 18px; color:#000; font-weight:regular">Curious about someone?<br>Just ask a mutual friend.</td><td width="200" height="120" bgcolor="FFFFFF" style="padding: 0px 0px 0px 20px"><img src="http://www.mymutuality.com/images/ask.jpg" alt="Image blocked" border="0"></td></tr></table></td></tr><tr><td><table cellpadding="0" cellspacing="0" width="460" bgcolor="FFFFFF"><tr><td width="460px" align="left" height="20px" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 20px 0px 20px 0px; font-size:16px; color:#000; font-weight:regular">Mutuality (finally) makes meeting cool people safe and simple.<br><br>If you have any questions about Mutuality, please reply to us at <a href="mailto:info@mymutuality.com">info@mymutuality.com</a>.<br><br>Thanks,<br><br>The Mutuality Team</td></tr></table></td></tr></table><table width="460" cellpadding="0" cellspacing="0" align="center" bgcolor="#FFFFFF"><tr><td width="50"></td><td width="410" align="right" height="30" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 6px; color:#DDD; font-weight:regular; border-top:1px solid #DDD">This email was sent by Mutuality. Mutuality helps you meet cool people through your mutual friends.<br>If you received this in error, please click <a href="#" style="color:#ccc">here</a> to unsubscribe.</td></tr></table></table></body></html>'''
    text = "Greetings,\n\nWelcome to Mutuality!\n\nOn Mutuality, you are connected to everyone you see. If you want to learn more about somebody, you can quickly ask a mutual friend about them.\n\nMutuality (finally) makes meeting cool people safe and simple.  If you have any questions or comments, please reply to us at info@mymutuality.com.\n\nBest,\n\nThe Mutuality Team"
    subject = "Welcome to Mutuality"
    from_header = from_address
    message = sendgrid.Message(from_header, subject, text, html)
    message.add_to(to_address, to_name)
    message.add_category([Email.WELCOME])
    return message


def create_friend_joined_message(from_address, to_address, to_name, friendName, friendFacebookID, numberOfNewFriends, totalNumberOfFriends, currentNumberOfFoF, city):
    estimatedFoFPotential = totalNumberOfFriends*10
    percentage = (currentNumberOfFoF*100/estimatedFoFPotential)
    oneMinusPercentage = 100-percentage
    html = '''<html><title>{0} joined you on Mutuality</title><body style = "margin:0px 0px 0px 0px; padding: 0px 0px 0px 0px; font-family: Tahoma, Geneva, sans-serif;"><!-- Start Header --><table width="560px" height="70" align="center" cellpadding="0px" cellspacing="0" bgcolor="#FFFFFF" style = "color:#000; font-weight: regular; padding: 0px 0px 0px 14px; font-family: Tahoma, Geneva, sans-serif;"><tr><td width="110px" height="70px"><a href="http://www.mymutuality.com?src=addFriendEmail_logo"><img src="http://www.mymutuality.com/images/smallLogo.jpg" width="95" height="40" alt="Logo" border="0"></a></td><td valign="bottom" width="410px" height="70px" style="font-size:14px; border-bottom: 1px solid #DDD; line-height:110%">{1} has joined you on Mutuality<br><br></td></tr></table><!-- End Header --><!-- Start Next Section --><table cellpadding="0" cellspacing="0" align="center" width="540px" bgcolor="FFFFFF"><tr><td width="120" height="130" align="right" valign="top" bgcolor="FFFFFF" style="padding:15px 0px 0px 0px"><img src="https://graph.facebook.com/{2}/picture?width=75&height=75"></td><td width="260" height="130" valign="top" align="right" cellspacing="0" bgcolor="FFFFFF" style="padding:15px 0px 0px 0px; font-size:14px">You are now connected to <span style="font-size:18px;font-weight:bold">{3}</span> more friends-of-friends in {4}<table width="400" height="100" align="right" cellpadding="0px" cellspacing="0" style="padding:0px 0px 0px 20px"><tr><td valign="bottom" height="40px"><table width="150px" height="20px" valign="bottom" align="left" cellpadding="0px" cellspacing="0"><tr><td width="{5}%" height="20px" bgcolor="#0065a5"></td><td width="{6}%" height="20px" bgcolor="#DDD"></td></tr></table></td><td valign="bottom" style="font-size:11px; padding:5px 0px 0px 20px">{7} network is now <span style="font-size:14px;font-weight:bold">{8}%</span> complete<br><a href="http://www.mymutuality.com?src=addFriendEmail_inviteFriendLink">Invite more friends</a></td><tr><td valign="top" style="font-size:9px">({9} connections out of {10})</td></tr></table></table><table width="560" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF"><tr><td width="50"></td><td width="410" align="right" height="30" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 6px; color:#DDD; font-weight:regular; border-top:1px solid #DDD">This email was sent by Mutuality. Mutuality helps you meet cool people through your mutual friends.<br>If you received this in error, please click <a href="#" style="color:#ccc">here</a> to unsubscribe.</td></tr><!-- </table> --></body></html>'''.format(friendName, friendName, friendFacebookID, numberOfNewFriends, city, percentage,oneMinusPercentage, city, percentage, currentNumberOfFoF, estimatedFoFPotential)
    text = "Greetings,\n\n{0} has joined you on Mutuality.\n\nYou are now connected to {1} more friends-of-friends in {2} for a total of {3} friends-of-friends in {4}. Your network is now {5} percent complete.\n\nBest,\n\nThe Mutuality Team".format(friendName,numberOfNewFriends,city,currentNumberOfFoF,city, percentage)
    subject = "(+{0}) {1} joined you on Mutuality".format(numberOfNewFriends, friendName)
    from_header = from_address
    message = sendgrid.Message(from_header, subject, text, html)
    message.add_to(to_address, to_name)
    message.add_category([Email.FRIEND_JOINED])
    return message


def create_inactive_message(from_address, to_address, to_name, new_friend_name, new_friend_facebookID, mutual_friend_count, mutual_friend_name):
    from_header = from_address
    newFriendFirstName = new_friend_name.split()[0]
    friend_string = 'friends'
    if mutual_friend_count == 1:
        friend_string = 'friend'
    subject = "You and {0} have {1} mutual {2}".format(newFriendFirstName, mutual_friend_count, friend_string)
    text = "Greetings,\n\nMeet {0}. You and {1} share {2} mutual friends including {3}.\n\nCheck out www.mymutuality.com to learn more about {4} and see 19 more friends-of-friends.\n\nBest,\n\nThe Mutuality Team".format(new_friend_name, newFriendFirstName, mutual_friend_count, mutual_friend_name, newFriendFirstName)
    html ='''<html><title>Have you met my friend {0}?</title><body style = "margin:0px 0px 0px 0px; padding: 0px 0px 0px 0px; font-family: Tahoma, Geneva, sans-serif;"><!-- Start Main Table --><table width = "100%" height="100%" cellpadding = "0" style="padding:10px 0px 10px 0px" bgcolor="#FFFFFF"><table align = "center" width="560px" height="35px" cellpadding="0px" cellspacing="0" bgcolor="#6ba4c5" style = "color:#FFFFFF; font-weight: regular; padding: 1px 0px 0px 14px; font-family: Tahoma, Geneva, sans-serif;"><tr><td><a href='http://www.mymutuality.com?src=email_inactive'><img src="http://www.mymutuality.com/images/LogoMedium.jpg" width="126" height="" alt="Logo" border="0"></a></td></tr></table><table width="560px" height = "200px" align="center"><tr><td width="340px" height="200px"><table cellpadding="0" cellspacing="0" width="340px" height="200px" bgcolor="FFFFFF"><tr><td bgcolor="FFFFFF" align="left" style="font-family: Tahoma, Geneva, sans-serif; padding: 5px 10px 0px 15px; font-size: 24px; color:#000; font-weight:regular">{1}</td></tr><tr><td align="left" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 10px 0px 15px; font-size: 12px; color:#000; font-weight:regular">You and {2} share <span style="font-size:18px; font-weight:bold">{3}</span> mutual friends including<br><span style="font-weight:bold">{4}.</span></td></tr></table></td><td width="200px" height="200px"><img src="https://graph.facebook.com/{5}/picture?width=160&height=160"></td></tr></table><table align="center"><tr><td align="center" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 10px 10px 20px 15px; font-size: 14px; color:#000; font-weight:regular"><a href="http://www.mymutuality.com?email_inactive-bottom">Click here</a> to learn more about {6} and see 19 more friends-of-friends</td></tr></table><table width="560" cellpadding="0" cellspacing="0" align="center" bgcolor="#FFFFFF"><tr><td width="50"></td><td width="410" align="right" height="30" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 6px; color:#DDD; font-weight:regular; border-top:1px solid #DDD">This email was sent by Mutuality. Mutuality helps you meet cool people through your mutual friends.<br>If you received this in error, please click <a href="#" style="color:#ccc">here</a> to unsubscribe.</td></tr></table></table></body></html>'''.format(newFriendFirstName, new_friend_name, newFriendFirstName, mutual_friend_count, mutual_friend_name, new_friend_facebookID, newFriendFirstName)
    message = sendgrid.Message(from_header, subject, text, html)
    message.add_to(to_address, to_name)
    message.add_category([Email.USER_INACTIVE])
    return message


def create_new_message_message(from_address, to_address, to_name, sender_name, mutualFriendNumber, mutual_friend_name):
    from_header = from_address
    sender_first_name = sender_name.split()[0]
    subject = "New message from {0}".format(sender_name)
    text = "Greetings,\n\n{0} just sent you a message on Mutuality. You and {1} share {2} mutual friends including {3}.\n\nView the message at www.mymutuality.com/messages.\n\nBest,\n\nThe Mutuality Team".format(sender_name, sender_first_name,mutualFriendNumber, mutual_friend_name)
    html = '''<html><title>New message from {0}</title><body style = "margin:0px 0px 0px 0px; padding: 0px 0px 0px 0px; font-family: Tahoma, Geneva, sans-serif;"><!-- Start Main Table --><table width = "560px" height="170px" align="center" cellpadding="0" cellspacing="0" style="padding:10px 0px 10px 0px" bgcolor="#FFFFFF"><tr height="35px"><td align = "left" width="560px" cellpadding="0px" cellspacing="0" bgcolor="#6ba4c5" style = "color:#FFFFFF; font-weight: regular; padding: 1px 0px 0px 14px; font-family: Tahoma, Geneva, sans-serif;"><a href='http://www.mymutuality.com?src=email_new-message'><img src="http://www.mymutuality.com/images/LogoMedium.jpg" width="126" height="" alt="Logo" border="0"></a></td></tr><tr><td bgcolor="FFFFFF" height="30px" width="560px" align="left" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 10px 0px 15px; font-size: 16px; color:#000; font-weight:regular">{1} just sent you a message on Mutuality</td></tr><tr><td align="left" height="20px" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 15px; font-size: 12px; color:#000; font-weight:regular">You and {2} share <span style="font-size:18px; font-weight:bold">{3}</span> mutual friends including <span style="font-weight:bold">{4}.</td></tr><tr><td align="left" height="30" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 15px 0px 15px; font-size: 16px; color:#000; font-weight:regular"><a href="http://www.mymutuality.com/messages?email_new-message">View the message on Mutuality</a></td></tr></table><table width="560" cellpadding="0" cellspacing="0" align="center" bgcolor="#FFFFFF"><tr><td width="50"></td><td width="410" align="right" height="30" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 6px; color:#DDD; font-weight:regular; border-top:1px solid #DDD">This email was sent by Mutuality. Mutuality helps you meet cool people through your mutual friends.<br>If you received this in error, please click <a href="#" style="color:#ccc">here</a> to unsubscribe.</td></tr></table></body></html>'''.format(sender_name, sender_name, sender_first_name, mutualFriendNumber, mutual_friend_name)
    message = sendgrid.Message(from_header, subject, text, html)
    message.add_to(to_address, to_name)
    message.add_category([Email.NEW_MESSAGE])
    return message
