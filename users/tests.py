from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson
from users.models import User, Payments


class UserTestCase(APITestCase):
    def setUp(self):
        pass

    def test_login_refresh(self):
        url1 = reverse('users:user_create')
        url2 = reverse('users:login')
        url3 = reverse('users:refresh')
        data1 = {'email': 'testuser10@gmail.com',
                 'password': '1234'}

        response1 = self.client.post(url1, data=data1)
        response2 = self.client.post(url2, data=data1)

        data2 = {'refresh': response2.data.get('refresh')}

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response2.data.get('access'), None)
        self.assertNotEqual(response2.data.get('refresh'), None)

        response3 = self.client.post(url3, data=data2)

        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response3.data.get('access'), None)

    def test_user_create_get(self):
        url1 = reverse('users:user_create')
        url2 = reverse('users:user_list')
        data = {'email': 'testuser10@gmail.com',
                'password': '1234'}
        response1 = self.client.post(url1, data=data)

        self.client.force_authenticate(user=User.objects.all().first())

        response2 = self.client.get(url2)
        data = response2.json()

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0].get('email'), 'testuser10@gmail.com')

    def test_user_detail_update_delete(self):
        url1 = reverse('users:user_create')
        data = {'email': 'testuser10@gmail.com',
                'password': '1234'}
        response1 = self.client.post(url1, data=data)
        self.client.force_authenticate(user=User.objects.all().first())

        url2 = reverse('users:user_detail', args=(response1.data.get('id'),))
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data.get('email'), 'testuser10@gmail.com')

        url3 = reverse('users:user_update', args=(response1.data.get('id'),))
        data2 = {'email': 'newtestuser10@gmail.com'}
        response3 = self.client.patch(url3, data=data2)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data.get('email'),
                         'newtestuser10@gmail.com')

        url4 = reverse('users:user_delete', args=(response1.data.get('id'),))
        response4 = self.client.delete(url4)
        self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)


class PaymentsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser10@gmail.com',
                                        password='1234')
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(title='test lesson',
                                            description='test description',
                                            owner=self.user)
        self.payments = Payments.objects.create(user=self.user,
                                                paid_lesson=self.lesson,
                                                date_of_payment='2024-08-21',
                                                payment_amount=10000,
                                                payment_method='CASH')

    def test_get_payments(self):
        url = reverse('users:payments_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0].get('paid_lesson'), self.lesson.id)
        self.assertEqual(data[0].get('date_of_payment'), '2024-08-21')
        self.assertEqual(data[0].get('payment_amount'), 10000)
        self.assertEqual(data[0].get('payment_method'), 'CASH')
