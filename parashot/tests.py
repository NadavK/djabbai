from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


class AssignmentTestCase(TransactionTestCase):
    fixtures = ['torahParasha', 'torahSegment']

    def setUp(self):
        User.objects.create_superuser(username='abc', password='test', email='admin@mail.com', first_name='ad', last_name='min')
        self.user1 = User.objects.create_user(username='abc', password='test', email='user1@mail.com', first_name='user', last_name='1')

    def test_parasha_permissions(self):
        anon = self.client
        response = anon.get(reverse('parasha-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = anon.put(reverse('parasha-detail', args=[1]), {"name": "name2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED
        response = anon.post(reverse('parasha-list'), {"name": "parasha1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED

        user = APIClient()
        login = user.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user.get(reverse('parasha-list'), {"name": "one2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user.put(reverse('parasha-detail', args=[1]), {"name": "name2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED
        response = user.post(reverse('parasha-list'), {"name": "one2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED

        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.get(reverse('parasha-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.put(reverse('parasha-detail', args=[1]), {"name": "name2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.post(reverse('parasha-list'), {"name": "parasha1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_segment_permissions(self):
        anon = self.client
        response = anon.get(reverse('segment-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED
        response = anon.put(reverse('segment-detail', args=[1]), {"name": "name2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED
        response = anon.post(reverse('segment-list'), {"name": "name1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED

        user = APIClient()
        login = user.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user.get(reverse('segment-list'), {"name": "one2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user.put(reverse('segment-detail', args=[1]), {"name": "name2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED
        response = user.post(reverse('segment-list'), {"name": "one2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED

        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.get(reverse('segment-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.put(reverse('segment-detail', args=[1]), {"parasha": 1, "segment_type": 1, "start_pos": "a", "end_pos": "b", "total_psukim": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.post(reverse('segment-list'), {"parasha": 1, "segment_type": 8, "start_pos": "a", "end_pos": "b", "total_psukim": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
