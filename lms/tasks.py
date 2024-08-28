from celery import shared_task

from lms.services import send_update_course


@shared_task
def task_update_course(course_id):
    """ Задача для автоматического отправления уведомления о изменении курса. """
    send_update_course(course_id)
