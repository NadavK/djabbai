from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
#from guardian.shortcuts import assign_perm, get_perms
from parashot.models import Parasha
from .models import Duty, Shabbat, Assignment, Roster
from users.models import Family, User
import datetime


class AssignmentTestCase(TransactionTestCase):
    fixtures = ['duties', 'torahParasha', 'torahSegment']

    def setUp(self):
        User.objects.create_superuser(username='abc', password='test', email='admin@mail.com', first_name='ad', last_name='min')
        self.user1 = User.objects.create_user(username='abc', password='test', email='user1@mail.com', first_name='user', last_name='1')
        self.user2 = User.objects.create_user(username='abc', password='test', email='user2@mail.com', first_name='user', last_name='2')
        self.user3 = User.objects.create_user(username='abc', password='test', email='user3@mail.com', first_name='user', last_name='3')

        self.sha0 = Shabbat.objects.create(dayt=datetime.date(2017, 9, 19), parasha=Parasha.objects.get(name='בראשית'))
        self.roster1 = Roster.objects.create(shabbat=self.sha0, duty=Duty.objects.get(name='ראשון'))
        self.roster2 = Roster.objects.create(shabbat=self.sha0, duty=Duty.objects.get(name='שני'))
        self.roster3 = Roster.objects.create(shabbat=self.sha0, duty=Duty.objects.get(name='שלישי'))
        self.ass11 = Assignment.objects.create(roster=self.roster1, user=self.user1)
        self.ass12 = Assignment.objects.create(roster=self.roster1, user=self.user2)
        self.ass21 = Assignment.objects.create(roster=self.roster2, user=self.user2)
        self.ass31 = Assignment.objects.create(roster=self.roster3, user=self.user3)

        print('SHABBAT', self.sha0)

    def test_duties(self):
        anon = self.client
        response = anon.get(reverse('duty-list'))                      # Get for No Family
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user1.get(reverse('duty-list'))                      # Get for No Family
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_spouse_errors_and_self_USER(self):
        #add self as spouse
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user1.get(reverse('user-spouse-list', args=[self.user1.pk]), format='json')                      # Get for No Family
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.get(reverse('user-spouse-list', args=[99]), format='json')                                 # Get for No User (No Spouse is checked elsewhere)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('user-spouse-detail', args=[self.user2.pk, self.user1.pk]), format='json')     # Bad user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('user-spouse-detail', args=[99, self.user1.pk]), format='json')                # Bad user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('user-spouse-detail', args=[self.user1.pk, 99]), format='json')                # Bad spouse
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('user-spouse-detail', args=[self.user1.pk, self.user1.pk]), format='json')     # self association is OK (creates family) (User cannot association existing spouse)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_associate_spouse_errors_and_self_ADMIN(self):
        #add self as spouse
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.get(reverse('user-spouse-list', args=[self.user1.pk]), format='json')                      # Get for No Family
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = admin.get(reverse('user-spouse-list', args=[99]), format='json')                                 # Get for No User (No Spouse is checked elsewhere)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = admin.put(reverse('user-spouse-detail', args=[99, self.user1.pk]), format='json')                # Bad user
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = admin.put(reverse('user-spouse-detail', args=[self.user1.pk, 99]), format='json')                # Bad spouse
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = admin.put(reverse('user-spouse-detail', args=[self.user1.pk, self.user1.pk]), format='json')     # self association is OK (creates family)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = admin.get(reverse('user-spouse-detail', args=[self.user1.pk, self.user1.pk]), format='json')     # Get for No Spouse
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = admin.get(reverse('user-spouse-list', args=[self.user1.pk]), format='json')                      # Get for No Spouse
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_associate_spouse_user(self):
        #User1 - add User3 as spouse
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user1.put(reverse('user-spouse-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_associate_spouse_admin(self):
        #Admin - add User3 as spouse
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.put(reverse('user-spouse-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = admin.get(reverse('user-spouse-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user3.username)
        response = admin.get(reverse('user-spouse-list', args=[self.user1.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user3.username)

    def test_assignment(self):
        #Anon
        anon = self.client
        response = anon.get(reverse('roster-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = anon.get(reverse('roster-detail', args=[self.roster1.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = anon.get(reverse('roster-assignment-list', args=[self.roster1.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = anon.get(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = anon.post(reverse('roster-list'), format='json', data={"shabbat": 1, "duty": 4})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = anon.post(reverse('roster-assignment-list', args=[self.roster1.pk]), format='json', data={"status": "OFFERED", "offer_type": "REGULAR", "user": 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = anon.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #User
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user1.get(reverse('roster-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.get(reverse('roster-detail', args=[self.roster1.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.get(reverse('roster-assignment-list', args=[self.roster1.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.get(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.get(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass21.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.get(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.get(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass12.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.get(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass11.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.get(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass21.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.post(reverse('roster-list'), format='json', data={"shabbat": 1, "duty": 4})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.post(reverse('roster-assignment-list', args=[self.roster1.pk]), format='json', data={"status": "OFFERED", "offer_type": "REGULAR", "user": 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user2 = APIClient()
        login = user2.login(username='user_2', password='test')
        self.assertEqual(login, True)
        response = user2.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user2.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_adminspouse_assignment(self):
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # Admin can associate spouse
        response = user1.put(reverse('user-spouse-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.put(reverse('user-spouse-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Parents cannot edit spouse assignments
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass31.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #self.assertEqual(response.data, {'non_field_errors': ['The fields roster, user must make a unique set.']})

    def test_adminchild_assignment(self):
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # Regular-User cannot associate child
        response = user1.put(reverse('user-child-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.post(reverse('user-child-detail', args=[self.user1.pk, self.user3.pk]) + 'associate/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Admin can associate child
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)

        #check if this is checked elsewhere. user 3 is not yet assocaited, so cannot be edited. in any case missing actual json data
        #response = admin.put(reverse('user-child-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        #self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = admin.post(reverse('user-child-detail', args=[self.user1.pk, self.user3.pk]) + 'associate/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Parents can edit child assignments
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass31.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #self.assertEqual(response.data, {'non_field_errors': ['The fields roster, user must make a unique set.']})

    def test_admin_stuff(self):         #not sure what, excactly
        # Admin
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.get(reverse('roster-list'), format='json')
        print('List:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.get(reverse('roster-detail', args=[self.roster1.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.get(reverse('roster-assignment-list', args=[self.roster1.pk]), format='json')
        print('roster1:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.get(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json')
        print('detail:', response.data)
        print('user1:', self.user1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.post(reverse('roster-list'), format='json', data={"shabbat": self.sha0.pk, "duty": 4})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = admin.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = admin.post(reverse('roster-assignment-list', args=[self.roster1.pk]), format='json', data={"status": "OFFERED", "offer_type": "REGULAR", "user": self.user3.pk})
        print('data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_userspouse_assignment(self):
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # User can create spouse
        response = user1.put(reverse('user-spouse-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.post(reverse('user-spouse-list', args=[self.user1.pk]), format='json', data={"first_name": "spouse1", "last_name": "last1", "username": "XXX"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        spouse1_pk = response.data['id']


        # Parents cannot edit spouse assignments
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": spouse1_pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass31.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #self.assertEqual(response.data, {'non_field_errors': ['The fields roster, user must make a unique set.']})

    def test_userchild_assignment(self):
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # User can create child
        response = user1.put(reverse('user-child-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.post(reverse('user-child-detail', args=[self.user1.pk, self.user3.pk]) + 'associate/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Parents can edit child assignments
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass21.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster2.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user3.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = user1.put(reverse('roster-assignment-detail', args=[self.roster3.pk, self.ass31.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = user1.put(reverse('roster-assignment-detail', args=[self.roster1.pk, self.ass11.pk]), format='json', data={"status": "CONFIRMED", "offer_type": "REGULAR", "user": self.user2.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #self.assertEqual(response.data, {'non_field_errors': ['The fields roster, user must make a unique set.']})

    def test_shabbat_get(self):
        # BAD Get
        response = self.client.get(reverse('shabbat-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       #status.HTTP_401_UNAUTHORIZED

        # User Get
        client = APIClient()
        login = client.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = client.get(reverse('shabbat-list'), format='json')
        #print('User1 response:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.content)
        #self.assertEqual(response.content, b'[{"url":"http://testserver/api/shabbats/2/","parasha":{"id":2,"name":"\xd7\x91\xd7\xa8\xd7\x90\xd7\xa9\xd7\x99\xd7\xaa"},"dayt":"2017-09-20","roster":[]}]')
        #self.assertEqual(response.content, b'[{"url":"http://testserver/api/shabbat/1/","parasha":{"url":"http://testserver/api/parasha/1/","name":"\xd7\x91\xd7\xa8\xd7\x90\xd7\xa9\xd7\x99\xd7\xaa"},"dayt":"2017-09-19","roster":[]}]')
