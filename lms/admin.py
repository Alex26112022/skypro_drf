from django.contrib import admin

from lms.models import Course, Lesson, SubscriptionToCourse

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(SubscriptionToCourse)
