from celery import task
from django.core.mail import send_mail

@task
def send_user_joined_email(profile):
	recipients = ['jeffreymames@gmail.com', 'jazjit.singh@gmail.com', 'kamran.munshi@gmail.com']
	subject = 'A New User Joined Mutuality!'
	message = '{0} joined Mutuality'.format(profile.name)

