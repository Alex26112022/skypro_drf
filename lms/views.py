from datetime import datetime, timedelta

from pytz import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from lms.models import Course, Lesson, SubscriptionToCourse
from lms.paginators import MyPaginator
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import task_update_course

tz = timezone('Europe/Moscow')
# Минимальное время обновления курса для отправки уведомления.
course_timedelta = timedelta(hours=4)


class CourseViewSet(ModelViewSet):
    """ Реализует CRUD для course. """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPaginator

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        elif self.action == 'update':
            self.permission_classes = [IsOwner | IsModerator]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated | IsModerator]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs.get('pk'))
        now = datetime.now(tz)
        if course and now - course.updated_at > course_timedelta:
            task_update_course.delay(kwargs.get('pk'))
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class LessonCreateApiView(CreateAPIView):
    """ Создает новый урок. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListApiView(ListAPIView):
    """ Возвращает список всех уроков. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveApiView(RetrieveAPIView):
    """ Возвращает информацию об уроке. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonUpdateApiView(UpdateAPIView):
    """ Редактирует урок. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner | IsModerator]

    def update(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs.get('pk'))
        now = datetime.now(tz)
        if lesson.course:
            if now - lesson.course.updated_at > course_timedelta:
                task_update_course.delay(lesson.course.pk)
            lesson.course.updated_at = now
            lesson.course.save()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class LessonDestroyApiView(DestroyAPIView):
    """ Удаляет урок. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class SubscriptionAPIView(APIView):
    """ Реализует подписку на курс. """

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = SubscriptionToCourse.objects.filter(course=course_item,
                                                        owner=user)
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            subs_item = SubscriptionToCourse.objects.create(course=course_item,
                                                            owner=user)
            message = 'подписка добавлена'

        return Response({"message": message})
