from celery import task
from django.core.mail import send_mail
import settings
import smtplib

@task
def send_user_joined_email(profile):
	recipients = ['jeffreymames@gmail.com', 'jazjit.singh@gmail.com', 'kamran.munshi@gmail.com']
	subject = 'A New User Joined Mutuality!'
	message = '{0} joined Mutuality'.format(profile.name)
	return send_mail(subject, message, 'info@mutuality.com', recipients, fail_silently=False)

def create_html_mail (html, text, subject, from_address):
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
    writer.addheader("From", from_address)
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
	server.sendmail(from_address, to_address, message)
	server.quit()

