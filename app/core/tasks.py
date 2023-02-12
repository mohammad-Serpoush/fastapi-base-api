from celery import shared_task


@shared_task
def task_celery():
    print("sample celery task")
    return 1
