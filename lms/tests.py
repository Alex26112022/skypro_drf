from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course, SubscriptionToCourse
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@mail.ru',
                                        password='1234')
        self.course = Course.objects.create(title='Test Course',
                                            description='test description',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson',
                                            description='test description',
                                            owner=self.user,
                                            course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_get_course(self):
        url = reverse('lms:course-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('results')[0].get('title'), 'Test Course')

    def test_get_course_detail(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test Course')
        self.assertEqual(data.get('description'), 'test description')

    def test_course_create(self):
        url = reverse('lms:course-list')
        data = {
            'title': 'Test Course 3',
            'description': 'test description 3',
            'owner': self.user.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)
        self.assertEqual(Course.objects.last().title, 'Test Course 3')

    def test_course_update(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {
            'title': 'Updated Test Course',
            'description': 'updated test description'
        }
        response = self.client.put(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Updated Test Course')
        self.assertEqual(data.get('description'), 'updated test description')

    def test_course_delete(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser2@mail.ru',
                                        password='1234')
        self.lesson = Lesson.objects.create(title='Test Lesson2',
                                            description='test description2',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_lesson(self):
        url = reverse('lms:lessons_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('results')[0].get('title'), 'Test Lesson2')

    def test_get_lesson_detail(self):
        url = reverse('lms:lessons_detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test Lesson2')
        self.assertEqual(data.get('description'), 'test description2')

    def test_lesson_create(self):
        url = reverse('lms:lesson_create')
        data = {
            'title': 'Test Lesson 3',
            'description': 'test description 3',
            'owner': self.user.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(Lesson.objects.last().title, 'Test Lesson 3')

    def test_lesson_update(self):
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {
            'title': 'Updated Test lesson',
            'description': 'updated test description'
        }
        response = self.client.put(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Updated Test lesson')
        self.assertEqual(data.get('description'), 'updated test description')

    def test_lesson_delete(self):
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionToCourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser3@mail.ru',
                                        password='1234')
        self.course = Course.objects.create(title='Test Course3',
                                            description='test description',
                                            owner=self.user)
        # self.subscription = SubscriptionToCourse(owner=self.user,
        #                                          course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_get_subscription(self):
        url = reverse('lms:subscription')
        data = {
            'course_id': self.course.pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
