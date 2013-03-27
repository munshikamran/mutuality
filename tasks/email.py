from celery import task
from django.core.mail import send_mail
from time import sleep

@task()
def sendEmail(sleepTime):
	sleep(sleepTime)
	return send_mail('Subject here', 'Here is the message.', 'from@example.com', ['jeffreymames@gmail.com'], fail_silently=False)