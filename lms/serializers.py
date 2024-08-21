from rest_framework.serializers import ModelSerializer, SerializerMethodField, \
    Serializer

from lms.models import Course, Lesson, SubscriptionToCourse
from lms.validators import InYoutube


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [InYoutube(field='video')]


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    is_subscription = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lessons(self, obj):
        return obj.lesson.count()

    def get_is_subscription(self, obj):
        return SubscriptionToCourse.objects.filter(course=obj,
                                                   owner=obj.owner).exists()
