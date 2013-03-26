from celery import task
# from time import sleep
# from django.core.mail import send_mail

@task()
def add(x, y):
    return x+y

@task()
def sendEmail():
	return send_mail('Subject here', 'Here is the message.', 'from@example.com', ['jeffreymames@gmail.com'], fail_silently=False)
