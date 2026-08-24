from time import sleep

from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    sleep(5)
    print("Я молодец")
