from celery import task
from django.core.mail import send_mail
import settings
import smtplib
from connect.functions import GetFriendIDs
from connect.models import Profile

def new_user_joined(profile):
    send_user_joined_email.delay(profile)
    send_welcome_email.delay(profile)
    # excute this in the future so we know that we already have the user's friendlist in the db
    send_friend_joined_email.apply_async(args=[profile], countdown=60)
    return True


@task
def send_user_joined_email(profile):
    recipients = ['jeffreymames@gmail.com', 'jazjit.singh@gmail.com', 'kamran.munshi@gmail.com']
    subject = 'A New User Joined Mutuality!'
    message = '{0} joined Mutuality'.format(profile.name)
    return send_mail(subject, message, 'info@mutuality.com', recipients, fail_silently=False)

@task
def send_welcome_email(profile):
    from_address = 'mutuality@myMutuality.com'
    to_address = profile.user.email
    message = create_welcome_message(from_address, to_address)
    return send_message(message, from_address, to_address)

@task
def send_friend_joined_email(joined_user_profile):
    from_address = 'mutuality@myMutuality.com'
    friendIDs = GetFriendIDs(joined_user_profile)
    friendsOnMutuality = Profile.objects.filter(facebookID__in=friendIDs)
    print friendsOnMutuality
    for profile in friendsOnMutuality:
        to_address = profile.user.email
        friendName = joined_user_profile.name
        friendFacebookID = joined_user_profile.facebookID
        numberOfNewFriends = 20
        totalNumberOfFriends = 30 
        currentNumberOfFoF = 100
        message = create_friend_joined_message(from_address, to_address, friendName, friendFacebookID, numberOfNewFriends, totalNumberOfFriends, currentNumberOfFoF)
        sent=send_message(message, from_address, to_address)
        print "send to".format(profile.name)




def create_html_mail (html, text, subject, from_header, to_header):
    """Create a mime-message that will render HTML in popular
    MUAs, text in better ones"""
    import MimeWriter
    import mimetools
    import cStringIO

    out = cStringIO.StringIO() # output buffer for our message 
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)

    writer = MimeWriter.MimeWriter(out)
    #
    # set up some basic headers... we put subject here
    # because smtplib.sendmail expects it to be in the
    # message body
    #
    writer.addheader("From", from_header)
    writer.addheader("To", to_header)
    writer.addheader("Subject", subject)
    writer.addheader("MIME-Version", "1.0")
    #
    # start the multipart section of the message
    # multipart/alternative seems to work better
    # on some MUAs than multipart/mixed
    #
    writer.startmultipartbody("alternative")
    writer.flushheaders()
    #
    # the plain text section
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'us-ascii')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()
    #
    # start the html subpart of the message
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    #
    # returns us a file-ish object we can write to
    #
    pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()
    #
    # Now that we're done, close our writer and
    # return the message body
    #
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    return msg

def send_message(message, from_address, to_address):
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    sent = server.sendmail(from_address, to_address, message)
    server.quit()
    return sent


# HTML messages
def create_welcome_message(from_address, to_address):
    html = '''<html><title>Welcome to Mutuality</title><body style = "margin:0px 0px 0px 0px;padding: 0px 0px 0px 0px; font-family: Tahoma, Geneva, sans-serif;"><!-- Start Main Table --><table width = "100%" height="100%" cellpadding = "0" style="padding:20px 0px 20px 0px" bgcolor="#FFFFFF"><table align="center"><tr><td width="460px" height="50px"><!-- Start Header --><table width="460px" cellpadding="0px" cellspacing="0" bgcolor="#6ba4c5" style = "color:#FFFFFF; font-weight: regular; padding: 16px 0px 16px 14px; font-family: Tahoma, Geneva, sans-serif;"><tr><td><a href='http://www.mymutuality.com?src=email_welcome'><img src="http://www.mymutuality.com/images/bigLogo.jpg" width="130" height="35" alt="Logo" border="0"></a></td></tr></table></td></tr></table><!-- End Header --><!-- Start Next Section --><table align="center"><tr><td width="460px" height="100px"><table cellpadding="0" cellspacing="0" width="460px" bgcolor="FFFFFF"><tr><td width="200" height="100" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 10px 10px 0px 15px; font-size: 16px; color:#000; font-weight:regular"><span style="font-size:34px; color:#989898; font-weight=regular">Welcome!</span><br><br>Creep.com? Never again.<br><br><br></td><td width="260" height="100" cellspacing="0" bgcolor="FFFFFF"><img src="http://www.mymutuality.com/images/carousel.jpg" alt="Image blocked" border="0"></td></tr></table></td></tr><tr><td><table cellpadding="0" cellspacing="0" width="460" bgcolor="FFFFFF"><tr><td width="200" height="120" bgcolor="FFFFFF" style="padding: 0px 0px 0px 20px"><img src="http://www.mymutuality.com/images/connected.jpg" alt="Image blocked" border="0"></td><td width="260" align="center" height="120" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 18px; color:#000; font-weight:regular">You are connected<br>to everyone you see.</td></tr></table></td></tr><tr><td><table cellpadding="0" cellspacing="0" width="460" bgcolor="FFFFFF"><tr><td width="260" align="center" height="120" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 18px; color:#000; font-weight:regular">Curious about someone?<br>Just ask a mutual friend.</td><td width="200" height="120" bgcolor="FFFFFF" style="padding: 0px 0px 0px 20px"><img src="http://www.mymutuality.com/images/ask.jpg" alt="Image blocked" border="0"></td></tr></table></td></tr><tr><td><table cellpadding="0" cellspacing="0" width="460" bgcolor="FFFFFF"><tr><td width="460px" align="left" height="20px" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 20px 0px 20px 0px; font-size:16px; color:#000; font-weight:regular">Mutuality (finally) makes meeting cool people safe and simple.<br><br>If you have any questions about Mutuality, please reply to us at <a href="mailto:info@mymutuality.com">info@mymutuality.com</a>.<br><br>Thanks,<br><br>The Mutuality Team</td></tr></table></td></tr></table><table width="460" cellpadding="0" cellspacing="0" align="center" bgcolor="#FFFFFF"><tr><td width="50"></td><td width="410" align="right" height="30" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 6px; color:#DDD; font-weight:regular; border-top:1px solid #DDD">This email was sent by Mutuality. Mutuality helps you meet cool people through your mutual friends.<br>If you received this in error, please click <a href="#" style="color:#ccc">here</a> to unsubscribe.</td></tr></table></table></body></html>'''
    text = "Greetings,\n\nWelcome to Mutuality!\n\nOn Mutuality, you are connected to everyone you see. If you want to learn more about somebody, you can quickly ask a mutual friend about them.\n\nMutuality (finally) makes meeting cool people safe and simple.  If you have any questions or comments, please reply to us at info@mymutuality.com.\n\nBest,\n\nThe Mutuality Team"
    subject = "Welcome to Mutuality"
    from_header = "Mutuality"
    return create_html_mail(html, text, subject, from_header, to_address)

def create_friend_joined_message(from_address, to_address, friendName, friendFacebookID, numberOfNewFriends, totalNumberOfFriends, currentNumberOfFoF):
    estimatedFoFPotential = totalNumberOfFriends*10
    percentage = (currentNumberOfFoF*100/estimatedFoFPotential)
    oneMinusPercentage = 100-percentage
    html = '''<html><title>{0} joined you on Mutuality</title><body style = "margin:0px 0px 0px 0px; padding: 0px 0px 0px 0px; font-family: Tahoma, Geneva, sans-serif;"><!-- Start Header --><table width="560px" height="70" align="center" cellpadding="0px" cellspacing="0" bgcolor="#FFFFFF" style = "color:#000; font-weight: regular; padding: 0px 0px 0px 14px; font-family: Tahoma, Geneva, sans-serif;"><tr><td width="110px" height="70px"><a href="http://www.mymutuality.com?src=addFriendEmail_logo"><img src="http://www.mymutuality.com/images/smallLogo.jpg" width="95" height="40" alt="Logo" border="0"></a></td><td valign="bottom" width="410px" height="70px" style="font-size:14px; border-bottom: 1px solid #DDD; line-height:110%">{1} has joined you on Mutuality<br><br></td></tr></table><!-- End Header --><!-- Start Next Section --><table cellpadding="0" cellspacing="0" align="center" width="540px" bgcolor="FFFFFF"><tr><td width="120" height="130" align="right" valign="top" bgcolor="FFFFFF" style="padding:15px 0px 0px 0px"><img src="https://graph.facebook.com/{2}/picture?width=75&height=75"></td><td width="260" height="130" valign="top" align="right" cellspacing="0" bgcolor="FFFFFF" style="padding:15px 0px 0px 0px; font-size:14px">You are now connected to <span style="font-size:18px;font-weight:bold">{3}</span> more friends-of-friends in Seattle<table width="400" height="100" align="right" cellpadding="0px" cellspacing="0" style="padding:0px 0px 0px 20px"><tr><td valign="bottom" height="40px"><table width="150px" height="20px" valign="bottom" align="left" cellpadding="0px" cellspacing="0"><tr><td width="{4}%" height="20px" bgcolor="#0065a5"></td><td width="{5}%" height="20px" bgcolor="#DDD"></td></tr></table></td><td valign="bottom" style="font-size:11px; padding:5px 0px 0px 20px">Seattle network is now <span style="font-size:14px;font-weight:bold">{6}%</span> complete<br><a href="http://www.mymutuality.com?src=addFriendEmail_inviteFriendLink">Invite more friends</a></td><tr><td valign="top" style="font-size:9px">({7} connections out of {8})</td></tr></table></table><table width="560" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF"><tr><td width="50"></td><td width="410" align="right" height="30" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 6px; color:#DDD; font-weight:regular; border-top:1px solid #DDD">This email was sent by Mutuality. Mutuality helps you meet cool people through your mutual friends.<br>If you received this in error, please click <a href="#" style="color:#ccc">here</a> to unsubscribe.</td></tr><!-- </table> --></body></html>'''.format(friendName, friendName, friendFacebookID, numberOfNewFriends, percentage,oneMinusPercentage, percentage, currentNumberOfFoF, estimatedFoFPotential)
    text = "Greetings,\n\n{0} has joined you on Mutuality.\n\nYou are now connected to {1} more friends-of-friends in Seattle for a total of {2} friends-of-friends in Seattle. Your network is now {3} percent complete.\n\nBest,\n\nThe Mutuality Team".format(friendName,numberOfNewFriends,currentNumberOfFoF,percentage)
    subject = "(+{0}) {1} joined you on Mutuality".format(numberOfNewFriends, friendName)
    from_header = "Mutuality"
    return create_html_mail(html, text, subject, from_header,to_address)

def create_inactive_message(to_address, newFriend, mutualFriendNumber, mutualFriendOne, mutualFriendTwo, mutualFriendThree):
    from_header = "Mutuality"
    newFriendFirstName = newFriend.name.split()[0]
    subject = "Have you met my friend {0} ({1})?".format(newFriendFirstName, mutualFriendNumber)
    text = "Greetings,\n\nMeet {0}. You and {1} share {2} mutual friends including {3}, {4}, and {5}.\n\nCheck out www.mymutuality.com to learn more about {6} and see 19 more friends-of-friends.\n\nBest,\n\nThe Mutuality Team".format(newFriend,newFriendFirstName,mutualFriendNumber, mutualFriendOne.name, mutualFriendTwo.name, mutualFriendThree.name,newFriendFirstName)
    html ='''<html><title>Have you met my friend {0}?</title><body style = "margin:0px 0px 0px 0px; padding: 0px 0px 0px 0px; font-family: Tahoma, Geneva, sans-serif;"><!-- Start Main Table --><table width = "100%" height="100%" cellpadding = "0" style="padding:10px 0px 10px 0px" bgcolor="#FFFFFF"><table align = "center" width="560px" height="35px" cellpadding="0px" cellspacing="0" bgcolor="#6ba4c5" style = "color:#FFFFFF; font-weight: regular; padding: 1px 0px 0px 14px; font-family: Tahoma, Geneva, sans-serif;"><tr><td><a href='http://www.mymutuality.com?src=email_inactive'><img src="http://www.mymutuality.com/images/LogoMedium.jpg" width="126" height="" alt="Logo" border="0"></a></td></tr></table><table width="560px" height = "200px" align="center"><tr><td width="340px" height="200px"><table cellpadding="0" cellspacing="0" width="340px" height="200px" bgcolor="FFFFFF"><tr><td bgcolor="FFFFFF" align="left" style="font-family: Tahoma, Geneva, sans-serif; padding: 5px 10px 0px 15px; font-size: 24px; color:#000; font-weight:regular">{1}</td></tr><tr><td align="left" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 10px 0px 15px; font-size: 12px; color:#000; font-weight:regular">You and {2} share <span style="font-size:18px; font-weight:bold">{3}</span> mutual friends including<br><span style="font-weight:bold">{4}, {5},</span> and <span style="font-weight:bold">{6}</span></td></tr><tr><td align="left" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 10px 10px 0px 15px; font-size: 12px; color:#000; font-weight:regular"><table cellpadding="0" cellspacing="0" width="340px" bgcolor="FFFFFF"><tr><td><img src = "https://graph.facebook.com/{7}/picture?width=75&height=75"></td><td><img src = "https://graph.facebook.com/{8}/picture?width=75&height=75"></td><td><img src = "https://graph.facebook.com/{9}/picture?width=75&height=75"></td></tr></table></td></tr></table></td><td width="200px" height="200px"><img src="https://graph.facebook.com/{10}/picture?width=160&height=160"></td></tr></table><table align="center"><tr><td align="center" bgcolor="FFFFFF" style="font-family: Tahoma, Geneva, sans-serif; padding: 10px 10px 20px 15px; font-size: 14px; color:#000; font-weight:regular"><a href="http://www.mymutuality.com?email_inactive-bottom">Click here</a> to learn more about {11} and see 19 more friends-of-friends</td></tr></table><table width="560" cellpadding="0" cellspacing="0" align="center" bgcolor="#FFFFFF"><tr><td width="50"></td><td width="410" align="right" height="30" style="font-family: Tahoma, Geneva, sans-serif; padding: 0px 0px 0px 0px; font-size: 6px; color:#DDD; font-weight:regular; border-top:1px solid #DDD">This email was sent by Mutuality. Mutuality helps you meet cool people through your mutual friends.<br>If you received this in error, please click <a href="#" style="color:#ccc">here</a> to unsubscribe.</td></tr></table></table></body></html>'''.format(newFriendFirstName, newFriend.name, newFriendFirstName, mutualFriendNumber, mutualFriendOne.name, mutualFriendTwo.name, mutualFriendThree.name,mutualFriendOne.facebookID, mutualFriendTwo.facebookID, mutualFriendThree.facebookID,newFriend.facebookID,newFriendFirstName)
    from_address = "info@mymutuality.com"
    message = create_html_mail(html, text, subject, from_header, to_address)
    return send_message (message, from_address, to_address)