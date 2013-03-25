from celery import task

@task()
def add(x, y):
    z = 0
    for i in range(1000000000):
        print 'jo'
        z = z + 1
    return z
