from celery import shared_task

from users.services import check_users_login_data


@shared_task
def task_period_check_users():
    """ Запускает периодически проверку пользователей. """
    check_users_login_data()
