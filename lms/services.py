from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Course, SubscriptionToCourse


def send_update_course(course_id):
    """ Отправка письма пользователю. """
    if Course.objects.get(pk=course_id):
        course = Course.objects.get(pk=course_id)
        subscription = SubscriptionToCourse.objects.filter(course=course)
        email_list = []
        if subscription.exists():
            print('Курс обновлен!')
            for subs in subscription:
                print(subs.owner.email)
                email_list.append(subs.owner.email)
            send_mail(subject='Обновление курса',
                      message=f'Курс {course} обновлен!',
                      from_email=EMAIL_HOST_USER,
                      recipient_list=email_list,
                      fail_silently=False)
