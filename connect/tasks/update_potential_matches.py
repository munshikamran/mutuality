from connect.functions.updatePotentialMatches import UpdatePotentialMatches
from connect.models.profile import Profile
from celery import task


def update_all_potential_matches():
    tasks = []
    for profile in Profile.objects.all():
        task = update_potential_matches_async.delay(profile)
        tasks.append(task)
    return tasks


@task
def update_potential_matches_async(profile):
    UpdatePotentialMatches(profile)
