from connect.models import Profile
from random import randint
from celery import task

@task
def send_welcome_message(profile):
	founder_ids = ['1240230066', '3900450', '1065870234']
	founder_profiles = Profile.objects.filter(facebookID__in=founder_ids)
	# get ransdm founder
	idx = random.randint(0, len(founder_profiles)-1)
	sender = founder_profiles[idx]
	first_name = sender.name.split(' ')[0]
	message = "Welcome! My name is {0} and I am one of the co-founders of Mutuality. I hope you enjoy the site and please stay in touch if you have any questions.".format(first_name)
	SendMessage(sender, profile.facebookID, message)




