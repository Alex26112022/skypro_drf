from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lessons(self, obj):
        return obj.lesson.count()
