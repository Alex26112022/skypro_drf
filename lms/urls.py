from django.urls import path

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter

from lms.views import CourseViewSet, LessonCreateApiView, LessonListApiView, \
    LessonRetrieveApiView, LessonDestroyApiView, LessonUpdateApiView

app_name = LmsConfig.name

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/', LessonListApiView.as_view(),
                       name='lessons_list'),
                  path('lesson/<int:pk>/', LessonRetrieveApiView.as_view(),
                       name='lessons_detail'),
                  path('lesson/create/', LessonCreateApiView.as_view(),
                       name='lesson_create'),
                  path('lesson/<int:pk>/update/',
                       LessonUpdateApiView.as_view(), name='lesson_update'),
                  path('lesson/<int:pk>/delete/',
                       LessonDestroyApiView.as_view(), name='lesson_delete'),
              ] + router.urls
