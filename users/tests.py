from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Profile, Family


class UserTestCase(TransactionTestCase):
    fixtures = ['duties', ]

    def setUp(self):
        from users.views import CheckUserThrottle
        CheckUserThrottle.rate='99/hour'
        from djabbai.settings import REST_FRAMEWORK
        REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['create'] = '99/hour'

        User.objects.create_superuser(username='abc', password='test', email='admin@mail.com', first_name='ad', last_name='min')
        Profile.objects.create(first_name='user', last_name='profile')        # this way the user-pk is different from the profile=pk
        self.user1 = User.objects.create_user(username='user_1', password='test', email='user1@mail.com', first_name='user', last_name='1')
        self.user2 = User.objects.create_user(username='user_2', password='test', email='user2@mail.com', first_name='user', last_name='2')
        self.user3 = User.objects.create_user(username='user_3', password='test', email='user3@mail.com', first_name='user', last_name='3')
        self.assertNotEqual(self.user1.pk,self.user1.profile.pk)

    # MANY SCENARIOS ARE TESTED IN ASSIGNMENT_TESTS!!!!

    def assertHttpCode(self, response, expected_code):
        """
        Prints the response data if the code is bad
        """
        self.assertEqual(response.status_code, expected_code, response.data)

    def assertHttpError(self, response):
        """
        Prints the response data if the code is bad
        """
        self.assertFalse(status.is_success(response.status_code), response.data)

    def test_case_insensitive_login(self):
        user = APIClient()
        login = user.login(username='user_1', password='testXXX')
        self.assertEqual(login, False)
        login = user.login(username='user_1', password='tesT')
        self.assertEqual(login, False)
        login = user.login(username='user_1', password='test')
        self.assertEqual(login, True)
        login = user.login(username='useR_1', password='test')
        self.assertEqual(login, True)

    def test_profile_permissions(self):
        anon = self.client
        #anon = APIClient()
        response = anon.get(reverse('profile-list'))
        self.assertHttpError(response)
        response = anon.get(reverse('profile-spouse-list', args=[self.user1.profile.pk]))
        self.assertHttpError(response)

        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user1.get(reverse('profile-list'))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)                                     # Only one object returned
        self.assertEqual(response.data[0]['id'], self.user1.profile.pk)

        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user1.profile.pk)
        response = user1.get(reverse('profile-detail', args=[self.user2.profile.pk]))
        self.assertHttpError(response)

        # No spouse
        response = user1.get(reverse('profile-spouse-list', args=[self.user1.profile.pk]))
        self.assertHttpError(response)
        response = user1.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]))
        self.assertHttpError(response)

        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.get(reverse('profile-list'))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)                                     # Number of profiles in the list
        response = admin.get(reverse('profile-spouse-list', args=[self.user1.profile.pk]))
        self.assertHttpError(response)

        response = admin.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = user1.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]))
        self.assertHttpError(response)

        # Associate spouse
        response = user1.put(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpError(response)
        response = admin.put(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)

        # User1 can now retrieve two profiles
        response = user1.get(reverse('profile-list'))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)                                     # Number of profiles in the list - now includes the spouse
        self.assertEqual(response.data[0]['id'], self.user1.profile.pk)
        self.assertEqual(response.data[1]['id'], self.user2.profile.pk)

        # But can now also retrieve the spouse
        response = user1.get(reverse('profile-spouse-list', args=[self.user1.profile.pk]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)                                     # Only one object returned
        self.assertEqual(response.data[0]['id'], self.user2.profile.pk)
        response = user1.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user2.profile.pk)
        response = user1.put(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]), format='json', data={'full_name': 'full spouse rename'})
        self.assertHttpError(response)      # Spouse is independent (has their own user) so cannot be edited even by other spouse
        response = user1.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user3.profile.pk]))
        self.assertHttpError(response)

        # And also admin
        response = admin.get(reverse('profile-spouse-list', args=[self.user1.profile.pk]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)                                     # Only one object returned
        self.assertEqual(response.data[0]['id'], self.user2.profile.pk)
        response = admin.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user2.profile.pk)
        response = user1.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user3.profile.pk]))
        self.assertHttpError(response)
        response = admin.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user3.profile.pk]))
        self.assertHttpCode(response, status.HTTP_200_OK)

    def test_register_new_user(self):
        anon = self.client

        # Bad password
        response = anon.post(reverse('user-create'), format='json', data={'username': 'new_user1', 'password': "123456", 'first_name': 'new', 'last_name': 'user1'})
        self.assertHttpCode(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'password': ['This password is too common.', 'This password is entirely numeric.']})

        # Bad password
        response = anon.post(reverse('user-create'), format='json', data={'username': 'new_user1', 'password': "abcdef", 'first_name': 'new', 'last_name': 'user1'})
        self.assertHttpCode(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'password': ['This password is too common.']})

        # No first_name
        response = anon.post(reverse('user-create'), format='json', data={'username': 'new_user1', 'password': "abcdef1", 'last_name': 'user1'})
        self.assertHttpCode(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'first_name': ['This field is required.']})

        # No last_name
        response = anon.post(reverse('user-create'), format='json', data={'username': 'new_user1', 'password': "abcdef1", 'first_name': 'new'})
        self.assertHttpCode(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'last_name': ['This field is required.']})

        # Everything OK
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'new', 'last_name': 'user1', 'full_name': 'full name'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)           #did we get a token?
        self.assertTrue(response.data['token'])         #is it empty?
        self.assertEqual(response.data['username'], 'new_user1')
        self.assertNotIn('read_only', response.data)

        # Check duplicate user
        response = anon.post(reverse('user-create'), format='json', data={'password': "abcdef1", 'first_name': 'new', 'last_name': 'user1', 'full_name': 'full name'})
        self.assertHttpError(response)

        # Check duplicate user w/bad username
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abv', 'password': "abcdef1", 'first_name': 'new', 'last_name': 'user1', 'full_name': 'full name'})
        self.assertHttpError(response)

        # Check duplicate profile
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abv', 'password': "abcdef1", 'first_name': 'user', 'last_name': 'profile', 'full_name': 'full name'})
        self.assertHttpError(response)

        # Check login works and that all data is valid
        user1 = self.client
        login = user1.login(username='new_user1', password='BadPassword')
        self.assertEqual(login, False)
        login = user1.login(username='new_user1', password='abcdef1')
        self.assertEqual(login, True)

        response = user1.get(reverse('get_current_profile'), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        #self.assertEqual(response.data['username'], 'new_user1')
        self.assertEqual(response.data['first_name'], 'new')
        self.assertEqual(response.data['last_name'], 'user1')
        self.assertEqual(response.data['display_name'], 'new user1')
        self.assertEqual(response.data.get('full_name'), None)        # Extra params are not saved by User. Need to call Profile API
        self.assertNotIn('read_only', response.data)


    def test_update_existing_user(self):
        anon = self.client

        # Everything OK
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'new', 'last_name': 'user1', 'full_name': 'full name'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)           #did we get a token?
        self.assertTrue(response.data['token'])         #is it empty?

        # Check login works and that all data is valid
        user1 = self.client
        login = user1.login(username='new_user1', password='BadPassword')
        self.assertEqual(login, False)
        login = user1.login(username='new_user1', password='abcdef1')
        self.assertEqual(login, True)

        response = user1.get(reverse('get_current_profile'), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        #self.assertEqual(response.data['username'], 'new_user1')
        self.assertEqual(response.data['first_name'], 'new')
        self.assertEqual(response.data['last_name'], 'user1')
        self.assertEqual(response.data['display_name'], 'new user1')
        self.assertEqual(response.data.get('full_name'), None)        # Extra params are not saved by User. Need to call Profile API

        # Update user (not via API)
        user = User.objects.get(pk=response.data['user'])
        user.first_name='newer'
        user.save()
        # Check that profile was updated
        response = user1.get(reverse('get_current_profile'), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'newer')

    def test_set_parents(self):
        #TODO: Add an existing parent-profile (per id) - not checked because there is no use-case for this

        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        user2 = APIClient()
        login = user2.login(username='user_2', password='test')
        self.assertEqual(login, True)

        # Check profile
        response = user1.get(reverse('get_current_profile'), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['display_name'], 'user 1')
        self.assertEqual(response.data.get('full_name'), None)
        self.assertEqual(response.data['first_name'], 'user')
        self.assertEqual(response.data['last_name'], '1')


        # Add first profile-details without father
        response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'first_name': 'firsta 1', 'full_name': 'my new name'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        patch_result = response.data
        self.assertEqual(response.data['first_name'], 'firsta 1')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['full_name'], 'my new name')
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertEqual(response.data.get('father'), None)
        self.assertEqual(response.data.get('mother'), None)
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data, patch_result)










        #TODO: Need to check default display_name
        #For parent's if display_name is empty, should be set to first_last









        # Add new profile for father - to wrong profile
        response = user1.patch(reverse('profile-detail', args=[self.user2.profile.pk]), format='json', data={'first_name': 'firsta 2', 'full_name': 'my name2', 'father': {'dod_month': '123', 'title': 'levi', 'gender': 'm', 'first_name': 'fatha 2', 'last_name': 'fatha 2', 'display_name': 'displa'}})
        self.assertHttpError(response)

        # Cannot add nested father profile
        response = user2.patch(reverse('profile-detail', args=[self.user2.profile.pk]), format='json', data={'first_name': 'firsta 2', 'full_name': 'my name2', 'father': {'dod_month': '123', 'title': 'levi', 'gender': 'm', 'first_name': 'fatha 2', 'last_name': 'fatha 2', 'display_name': 'displa'}})
        self.assertHttpCode(response, status.HTTP_200_OK)
        patch_result = response.data
        self.assertEqual(response.data['first_name'], 'firsta 2')
        self.assertEqual(response.data['last_name'], '2')
        self.assertEqual(response.data['full_name'], 'my name2')
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertEqual(response.data['display_name'], 'firsta 2 2')
        self.assertNotIn('parent', response.data)
        response = user2.get(reverse('profile-detail', args=[self.user2.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data, patch_result)

        # Add new profile for father with bad data
        response = user2.post(reverse('profile-parent-list', args=[self.user2.profile.pk]), format='json', data={'dod_month': '12', 'title': 'levi', 'gender': 'm'})
        self.assertHttpError(response)

        # Add new profile for father
        response = user2.post(reverse('profile-parent-list', args=[self.user2.profile.pk]), format='json', data={'dod_month': '12', 'title': 'levi', 'gender': 'm', 'full_name': 'fully'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertNotIn('first_name', response.data)
        self.assertNotIn('last_name', response.data)
        self.assertEqual(response.data['full_name'], 'fully')
        self.assertEqual(response.data['display_name'], 'fully')
        self.assertEqual(response.data['title'], 'levi')
        self.assertEqual(response.data['dod_month'], 12)
        parent1_pk = response.data['id']
        father_family_pk = response.data['default_family_to_add_children']
        parent_result = response.data

        response = user2.get(reverse('profile-detail', args=[self.user2.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'firsta 2')
        self.assertEqual(response.data['last_name'], '2')
        self.assertEqual(response.data['full_name'], 'my name2')
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertEqual(response.data['parents'][0], parent_result)

        #Edit father profile directly
        response = user2.patch(reverse('profile-detail', args=[parent1_pk]), format='json', data={'first_name': 'fatha 2b', 'last_name': 'fatha L2b'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        parent_result = response.data
        self.assertEqual(response.data['id'], parent1_pk)
        self.assertEqual(response.data['first_name'], 'fatha 2b')
        self.assertEqual(response.data['title'], 'levi')
        self.assertEqual(response.data['dod_month'], 12)
        self.assertEqual(response.data['display_name'], 'fatha 2b fatha L2b')

        response = user2.get(reverse('profile-detail', args=[self.user2.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'firsta 2')
        self.assertEqual(response.data['last_name'], '2')
        self.assertEqual(response.data['full_name'], 'my name2')
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertEqual(response.data['display_name'], 'firsta 2 2')
        del parent_result['children']       # remove children from comparision, because children are not returned as part of nested parent
        self.assertEqual(response.data['parents'][0], parent_result)



        # Add new profile for mother
        response = user2.post(reverse('profile-parent-list', args=[self.user2.profile.pk]), format='json', data={'dod_month': '13', 'title': 'levi', 'gender': 'f', 'full_name': 'fuller'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertNotIn('first_name', response.data)
        self.assertNotIn('last_name', response.data)
        self.assertEqual(response.data['display_name'], 'fuller')
        self.assertEqual(response.data['title'], 'levi')
        self.assertEqual(response.data['dod_month'], 13)
        self.assertEqual(response.data['default_family_to_add_children'], father_family_pk)
        parent1_pk2 = response.data['id']
        #parent_result = response.data

        # Check Family
        family = Family.objects.get(id=father_family_pk)
        self.assertCountEqual(family.parents.all().values_list('id', flat=True), [parent1_pk, parent1_pk2])     # Count compares elements
        self.assertIn(self.user2.profile.pk, family.children.all().values_list('id', flat=True))


    def test_full_aliya_names(self):
        #TODO: test with female profiles (and father is Cohen/levi)

        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # Check empty full_name
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data.get('full_name'), None)
        self.assertEqual(response.data.get('full_aliya_name'), None)

        # Add full_name
        response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'full_name': 'שם מלא', 'title': 'levi'})
        #response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'full_name': 'שם מלא', 'title': 'levi', 'father': {'title': 'levi', 'first_name': 'fatha 2', 'last_name': 'fatha 2', 'display_name': 'displa father'}})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'levi')
        self.assertEqual(response.data['full_name'], 'שם מלא')
        self.assertEqual(response.data['full_aliya_name'], 'שם מלא הלוי')
        self.assertEqual(response.data.get('father'), None)

        # Add Levi - nested object is ignored
        response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'father': {'title': 'levi', 'first_name': 'fatha 2', 'last_name': 'fathar 2', 'full_name': 'שמי אבא'}})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'levi')
        self.assertEqual(response.data['full_name'], 'שם מלא')
        self.assertEqual(response.data['full_aliya_name'], 'שם מלא הלוי')
        self.assertNotIn('father', response.data)

        # Add Levi Father
        response = user1.post(reverse('profile-parent-list', args=[self.user1.profile.pk]), format='json', data= {'title': 'levi', 'full_name': 'שמי אבא'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertNotIn('first_name', response.data)
        self.assertNotIn('last_name', response.data)
        self.assertEqual(response.data['full_name'], 'שמי אבא')
        self.assertEqual(response.data['full_aliya_name'], 'שמי אבא הלוי')
        father_id = response.data['id']

        # Add Levi Father
        response = user1.patch(reverse('profile-detail', args=[father_id]), format='json', data= {'gender': 'm', 'title': 'levi', 'first_name': 'fatha 2', 'last_name': 'fathar 2', 'full_name': 'שמי אבא'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'fatha 2')
        self.assertEqual(response.data['last_name'], 'fathar 2')
        self.assertEqual(response.data['full_name'], 'שמי אבא')
        self.assertEqual(response.data['full_aliya_name'], 'שמי אבא הלוי')

        # Get updated deep
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'levi')
        self.assertEqual(response.data['full_name'], 'שם מלא')
        self.assertEqual(response.data['full_aliya_name'], 'שם מלא בן שמי אבא הלוי')
        self.assertEqual(response.data['parents'][0]['first_name'], 'fatha 2')
        self.assertEqual(response.data['parents'][0]['last_name'], 'fathar 2')
        self.assertEqual(response.data['parents'][0]['full_name'], 'שמי אבא')
        self.assertEqual(response.data['parents'][0]['full_aliya_name'], 'שמי אבא הלוי')

        # Edit Levi - nested object is ignored
        response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'father': {'title': 'levi', 'first_name': 'fatha 2', 'last_name': 'fathaX 2', 'full_name': 'שמי אבאedited'}})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'levi')
        self.assertEqual(response.data['full_name'], 'שם מלא')
        self.assertEqual(response.data['full_aliya_name'], 'שם מלא בן שמי אבא הלוי')
        self.assertEqual(response.data['parents'][0]['first_name'], 'fatha 2')
        self.assertEqual(response.data['parents'][0]['last_name'], 'fathar 2')
        self.assertEqual(response.data['parents'][0]['full_name'], 'שמי אבא')
        self.assertEqual(response.data['parents'][0]['full_aliya_name'], 'שמי אבא הלוי')

        # Edit Levi profile directly
        response = user1.patch(reverse('profile-detail', args=[father_id]), format='json', data={'full_name': 'שמי אבאedited'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'fatha 2')
        self.assertEqual(response.data['last_name'], 'fathar 2')
        self.assertEqual(response.data['full_name'], 'שמי אבאedited')
        self.assertEqual(response.data['full_aliya_name'], 'שמי אבאedited הלוי')

        # get user deep
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'title': 'levi', 'first_name': 'fatha 2', 'last_name': 'fatha 2', 'full_name': 'שמי אבא'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'levi')
        self.assertEqual(response.data['full_name'], 'שם מלא')
        self.assertEqual(response.data['full_aliya_name'], 'שם מלא בן שמי אבאedited הלוי')
        self.assertEqual(response.data['parents'][0]['first_name'], 'fatha 2')
        self.assertEqual(response.data['parents'][0]['last_name'], 'fathar 2')
        self.assertEqual(response.data['parents'][0]['full_name'], 'שמי אבאedited')
        self.assertEqual(response.data['parents'][0]['full_aliya_name'], 'שמי אבאedited הלוי')

        # Directly edit the fathers profile
        response = user1.patch(reverse('profile-detail', args=[father_id]), format='json', data={'title': 'levi', 'full_name': 'שמי אבא', 'father_full_name': 'סבאבא'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'שמי אבא')
        self.assertEqual(response.data['father_full_name'], 'סבאבא')
        self.assertEqual(response.data['full_aliya_name'], 'שמי אבא בן סבאבא הלוי')
        self.assertEqual(response.data['children'][0]['full_name'], 'שם מלא')
        self.assertEqual(response.data['children'][0]['full_aliya_name'], 'שם מלא בן שמי אבא הלוי')

        # and check that it is updated also in the child deep
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['parents'][0]['full_name'], 'שמי אבא')
        self.assertEqual(response.data['parents'][0]['full_aliya_name'], 'שמי אבא בן סבאבא הלוי')

    # Test Duties
    def test_duties_kiddush(self):
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # non-household profiles are not assigned kiddush duty
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json')
        self.assertNotIn('duties', response.data)

        # household profiles are automatically assigned kiddush duty
        response = user1.put(reverse('profile-detail', args=[self.user1.profile.pk]), data={'head_of_household': True}, format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json')
        self.assertEqual(response.data['duties'], [19])

        response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'duties': [1,2]})
        self.assertEqual(response.data['duties'], [1, 2, 19])

        response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'full_name': 'new name'})
        self.assertEqual(response.data['full_name'], 'new name')
        self.assertEqual(response.data['duties'], [1, 2, 19])

        response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'duties': []})
        self.assertEqual(response.data['duties'], [19])

        response = user1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'duties': {}})
        self.assertEqual(response.data['duties'], [19])


    def test_add_spouse(self):
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # Cannot create spouse for other profile
        response = user1.post(reverse('profile-spouse-list', args=[1]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1'})
        self.assertHttpError(response)
        #self.assertEqual(response.data, {'detail': 'You do not have permission to perform this action.'})

        # Cannot create spouse for non-existing profile
        response = user1.post(reverse('profile-spouse-list', args=[99]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1'})
        self.assertHttpError(response)

        # Create spouse with bad fields
        response = user1.post(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx'})
        self.assertHttpError(response)

        # Create spouse
        response = user1.post(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'spouse')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'spouse 1')
        self.assertNotIn('full_name', response.data)
        self.assertEqual(response.data['title'], 'yisrael')
        spouse_pk = response.data['id']

        # Get spouse detail
        response = user1.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, spouse_pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'spouse')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'spouse 1')
        self.assertNotIn('full_name', response.data)
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertEqual(response.data['id'], spouse_pk)

        # Get spouse detail from deep profile
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['spouse']['first_name'], 'spouse')
        self.assertEqual(response.data['spouse']['last_name'], '1')
        self.assertEqual(response.data['spouse']['display_name'], 'spouse 1')
        self.assertNotIn('full_name', response.data)
        self.assertEqual(response.data['spouse']['title'], 'yisrael')

        # Get spouse list
        response = user1.get(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)                                     # Only one object returned
        self.assertEqual(response.data[0]['first_name'], 'spouse')
        self.assertEqual(response.data[0]['last_name'], '1')
        self.assertEqual(response.data[0]['display_name'], 'spouse 1')
        self.assertNotIn('full_name', response.data[0])
        self.assertEqual(response.data[0]['title'], 'yisrael')
        spouse_pk = response.data[0]['id']

        # Try adding another spouse
        response = user1.post(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1'})
        self.assertHttpError(response)
        self.assertEqual(response.data, ['Profile already has spouse'])

        # Edit spouse
        response = user1.patch(reverse('profile-spouse-detail', args=[self.user1.profile.pk, spouse_pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'spouse')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'spouse 1')
        self.assertEqual(response.data['full_name'], 'full spouse')
        self.assertEqual(response.data['title'], 'yisrael')

        # TODO: test editing on the profile API


    def test_associating_spouse(self):
        # Regular user cannot associate existing profile as a spouse
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user1.put(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpError(response)

        # Only Admin can associate a spouse to a profile
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.put(reverse('profile-spouse-detail', args=[self.user1.profile.pk, self.user2.profile.pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)

        response = admin.get(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)                                     # Only one object returned
        self.assertEqual(response.data[0]['first_name'], 'user')
        self.assertEqual(response.data[0]['last_name'], '2')
        self.assertEqual(response.data[0]['display_name'], 'user 2')
        self.assertEqual(response.data[0].get('full_name'), None)            #the put only associated the user - did not change the fields
        self.assertEqual(response.data[0]['title'], 'yisrael')

    def test_add_child(self):
        # Note: Also checks registering a spouse (creating a user from a profile)
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # Cannot create child for other profile
        response = user1.post(reverse('profile-child-list', args=[1]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child1', 'last_name': '1'})
        self.assertHttpError(response)
        self.assertEqual(response.data, {'detail': 'You do not have permission to perform this action.'})

        # Cannot create child for non-existing profile
        response = user1.post(reverse('profile-child-list', args=[99]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child1', 'last_name': '1'})
        self.assertHttpError(response)

        # Create child with bad fields
        response = user1.post(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx'})
        self.assertHttpError(response)

        # Create child
        response = user1.post(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child1', 'last_name': '1'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'child1')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'child1 1')
        self.assertNotIn('full_name', response.data)
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertNotIn('read_only', response.data)
        child1_pk = response.data['id']
        child1_verification_code = response.data['verification_code']

        # Get child detail
        response = user1.get(reverse('profile-child-detail', args=[self.user1.profile.pk, child1_pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'child1')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'child1 1')
        self.assertNotIn('full_name', response.data)
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertEqual(response.data['id'], child1_pk)
        self.assertNotIn('read_only', response.data)
        self.assertEqual(response.data['verification_code'], child1_verification_code)
        self.assertEqual(len(response.data['parents']), 1)
        self.assertEqual(response.data['parents'][0]['id'], self.user1.profile.pk)

        # Get child detail from deep profile
        response = user1.get(reverse('profile-list'), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)                                     # User can now also retrieve the child
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['children'][0]['first_name'], 'child1')
        self.assertEqual(response.data['children'][0]['last_name'], '1')
        self.assertEqual(response.data['children'][0]['display_name'], 'child1 1')
        self.assertEqual(response.data['children'][0].get('full_name'), None)
        self.assertEqual(response.data['children'][0]['title'], 'yisrael')
        self.assertNotIn('read_only', response.data['children'][0])

        # Get children list
        response = user1.get(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)                                     # Only one object returned
        self.assertEqual(response.data[0]['first_name'], 'child1')
        self.assertEqual(response.data[0]['last_name'], '1')
        self.assertEqual(response.data[0]['display_name'], 'child1 1')
        self.assertNotIn('full_name', response.data[0])
        self.assertEqual(response.data[0]['title'], 'yisrael')
        self.assertEqual(response.data[0]['id'], child1_pk)
        self.assertNotIn('read_only', response.data[0])

        # Try adding another child
        response = user1.post(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child2', 'last_name': '1'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'child2')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'child2 1')
        self.assertNotIn('full_name', response.data)
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertNotIn('read_only', response.data)
        child2_pk = response.data['id']

        # Get child detail from deep profile
        response = user1.get(reverse('profile-list'), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)                                     # User can now also retrieve both children
        response = user1.get(reverse('profile-detail', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['children'][0]['first_name'], 'child1')
        self.assertEqual(response.data['children'][0]['last_name'], '1')
        self.assertEqual(response.data['children'][0]['display_name'], 'child1 1')
        self.assertEqual(response.data['children'][0].get('full_name'), None)
        self.assertEqual(response.data['children'][0]['title'], 'yisrael')
        self.assertNotIn('read_only', response.data['children'][0])
        self.assertEqual(response.data['children'][0]['id'], child1_pk)

        self.assertEqual(response.data['children'][1]['first_name'], 'child2')
        self.assertEqual(response.data['children'][1]['last_name'], '1')
        self.assertEqual(response.data['children'][1]['display_name'], 'child2 1')
        self.assertEqual(response.data['children'][1].get('full_name'), None)
        self.assertEqual(response.data['children'][1]['title'], 'yisrael')
        self.assertNotIn('read_only', response.data['children'][1])
        self.assertEqual(response.data['children'][1]['id'], child2_pk)

        # Get children list
        response = user1.get(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)                                     # Two children

        # Edit child
        response = user1.patch(reverse('profile-child-detail', args=[self.user1.profile.pk, child2_pk]), format='json', data={'full_name': 'full child2'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'child2')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'child2 1')
        self.assertEqual(response.data['full_name'], 'full child2')
        self.assertEqual(response.data['title'], 'yisrael')
        self.assertNotIn('read_only', response.data)



        anon = APIClient()
        # Create user for existing child profile - without verification
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child1', 'last_name': '1', 'full_name': 'full name'})
        self.assertHttpError(response)

        # Create user for existing child profile - with wrong verification
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child1', 'last_name': '1', 'full_name': 'full name', 'verification_code': 123})
        self.assertHttpError(response)

        # Create user for existing child profile - with correct verification
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child1New', 'last_name': '1New', 'full_name': 'full name', 'verification_code': child1_verification_code})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'child1New')
        self.assertEqual(response.data['last_name'], '1New')
        self.assertIn('token', response.data)                   #did we get a token?
        self.assertTrue(response.data['token'])                 #is it empty?
        self.assertEquals(response.data['id'], child1_pk)       #is is the profile-id
        child1_user_pk = response.data['user']                  #This is the user-id

        response = user1.get(reverse('profile-child-detail', args=[self.user1.profile.pk, child1_pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], child1_user_pk)
        self.assertEqual(response.data['read_only'], True)
        self.assertNotIn('verification_code', response.data)       # User is verified, so verification-code no longer exists

        # Verified (registered) child cannot be edited by parent
        response = user1.patch(reverse('profile-child-detail', args=[self.user1.profile.pk, child1_pk]), format='json', data={'full_name': 'full child1 edit'})
        self.assertHttpError(response)
        response = user1.patch(reverse('profile-detail', args=[child1_pk]), format='json', data={'full_name': 'full child1 edit'})
        self.assertHttpError(response)

        # Verified (registered) parent cannot be edited by child
        child1 = APIClient()
        self.assertFalse(child1.login(username='child1_1', password='abcdef1'))
        self.assertTrue(child1.login(username='child1New_1New', password='abcdef1'))
        response = child1.get(reverse('get_current_profile'), format='json')
        self.assertEqual(response.data['parents'][0]['read_only'], True)
        response = child1.patch(reverse('profile-parent-detail', args=[child1_pk, self.user1.profile.pk]), format='json', data={'full_name': 'full child1 edit'})
        self.assertHttpError(response)
        response = child1.patch(reverse('profile-detail', args=[self.user1.profile.pk]), format='json', data={'full_name': 'full child1 edit'})
        self.assertHttpError(response)


        # Add mother/spouse and ensure all children are referenced
        response = user1.post(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json',
                              data={'username': 'abx', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'spouse')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'spouse 1')
        self.assertNotIn('full_name', response.data)
        self.assertEqual(response.data['title'], 'yisrael')
        spouse_pk = response.data['id']
        spouse_verification_code = response.data['verification_code']


        # Get children list
        response = user1.get(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)                                     # Two children



        # Get spouse detail
        response = user1.get(reverse('profile-spouse-detail', args=[self.user1.profile.pk, spouse_pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'spouse')
        self.assertEqual(response.data['last_name'], '1')
        self.assertEqual(response.data['display_name'], 'spouse 1')
        self.assertNotIn('full_name', response.data)
        self.assertEqual(response.data['title'], 'yisrael')



        # Get child detail from deep profile
        response = user1.get(reverse('profile-list'), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)                                     # User can now also retrieve both children
        response = user1.get(reverse('profile-detail', args=[spouse_pk]), format='json')                #using spouse details!!!!
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['children'][0]['first_name'], 'child1New')
        self.assertEqual(response.data['children'][0]['last_name'], '1New')
        self.assertEqual(response.data['children'][0]['display_name'], 'child1New 1New')
        self.assertEqual(response.data['children'][0].get('full_name'), None)
        self.assertEqual(response.data['children'][0]['title'], 'yisrael')
        self.assertEqual(response.data['children'][0]['read_only'], True)
        self.assertEqual(response.data['children'][0]['id'], child1_pk)

        self.assertEqual(response.data['children'][1]['first_name'], 'child2')
        self.assertEqual(response.data['children'][1]['last_name'], '1')
        self.assertEqual(response.data['children'][1]['display_name'], 'child2 1')
        self.assertEqual(response.data['children'][1].get('full_name'), 'full child2')
        self.assertEqual(response.data['children'][1]['title'], 'yisrael')
        self.assertNotIn('read_only', response.data['children'][1])
        self.assertEqual(response.data['children'][1]['id'], child2_pk)

        # Create user for existing spouse profile - with correct verification
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1', 'full_name': 'full name', 'verification_code': spouse_verification_code})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)                   #did we get a token?
        self.assertTrue(response.data['token'])                 #is it empty?
        self.assertEqual(response.data['id'], spouse_pk)

        spouse1 = APIClient()
        login = spouse1.login(username='spouse_1', password='abcdef1')
        self.assertEqual(login, True)

        # Get child detail from deep profile
        response = spouse1.get(reverse('profile-list'), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        #self.assertEqual(len(response.data), 4)                                     # User can now also retrieve both children
        response = spouse1.get(reverse('profile-detail', args=[spouse_pk]), format='json')                #using spouse details!!!!
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['children'][0]['first_name'], 'child1New')
        self.assertEqual(response.data['children'][0]['last_name'], '1New')
        self.assertEqual(response.data['children'][0]['display_name'], 'child1New 1New')
        self.assertEqual(response.data['children'][0].get('full_name'), None)
        self.assertEqual(response.data['children'][0]['title'], 'yisrael')
        self.assertEqual(response.data['children'][0]['read_only'], True)
        self.assertEqual(response.data['children'][0]['id'], child1_pk)

        self.assertEqual(response.data['children'][1]['first_name'], 'child2')
        self.assertEqual(response.data['children'][1]['last_name'], '1')
        self.assertEqual(response.data['children'][1]['display_name'], 'child2 1')
        self.assertEqual(response.data['children'][1].get('full_name'), 'full child2')
        self.assertEqual(response.data['children'][1]['title'], 'yisrael')
        self.assertNotIn('read_only', response.data['children'][1])
        self.assertEqual(response.data['children'][1]['id'], child2_pk)




    # TODO: test editing on the profile API


    def DISABLED_test_throttle_check_user(self):       #Disabled because it affected other tests
        anon = self.client

        for x in range(15):
            response = anon.get(reverse('check_user', args=['user', '1']))  # Newly created user
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = anon.get(reverse('check_user', args=['user', '1']))      # Newly created user
        self.assertHttpCode(response, status.HTTP_429_TOO_MANY_REQUESTS)

    def DISABLED_test_throttle_user_create(self):       #Disabled because it affected other tests
        anon = self.client
        for x in range(15):
            response = anon.post(reverse('user-create'), format='json', data={'password': "abcdef1", 'first_name': 'user', 'last_name': 'profile', 'verification_code': 123})
            self.assertHttpCode(response, status.HTTP_400_BAD_REQUEST)
        response = anon.post(reverse('user-create'), format='json', data={'password': "abcdef1", 'first_name': 'user', 'last_name': 'profile', 'verification_code': 123})
        self.assertHttpCode(response, status.HTTP_429_TOO_MANY_REQUESTS)

    def DISABLED_test_throttle_create_profile(self):       #Disabled because it affected other tests
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        for x in range(15):
            response = user1.post(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx'})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = user1.post(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx'})
        self.assertHttpCode(response, status.HTTP_429_TOO_MANY_REQUESTS)

        response = user1.post(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx'})
        self.assertHttpCode(response, status.HTTP_429_TOO_MANY_REQUESTS)

        response = user1.post(reverse('profile-parent-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx'})
        self.assertHttpCode(response, status.HTTP_429_TOO_MANY_REQUESTS)


    def test_check_user(self):
        # test the check_user API
        anon = self.client
        response = anon.get(reverse('check_user', args=['user', '1']))      # Newly created user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True, 'verified': True})

        response = anon.get(reverse('check_user', args=['User', '1']))      # Newly created user - case-insensitive
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True, 'verified': True})

        response = anon.get(reverse('check_user', args=['spouse', '1']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': False})

        response = anon.get(reverse('check_user', args=['Spouse', '1']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': False})

        response = anon.get(reverse('check_user', args=['child1', '1']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': False})

        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # Create spouse
        response = user1.post(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1'})
        user1_verification_code = response.data['verification_code']
        self.assertHttpCode(response, status.HTTP_201_CREATED)

        response = anon.get(reverse('check_user', args=['spouse', '1']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True, 'family': 'user & spouse 1', 'relation': 'spouse', 'verified': False, 'verification_code': False})

        response = anon.get(reverse('check_user', args=['spouse', '1', None]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True, 'family': 'user & spouse 1', 'relation': 'spouse', 'verified': False, 'verification_code': False})

        response = anon.get(reverse('check_user', args=['spouse', '1', '']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True, 'family': 'user & spouse 1', 'relation': 'spouse', 'verified': False, 'verification_code': False})

        response = anon.get(reverse('check_user', args=['spouse', '1', 1234567]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True, 'family': 'user & spouse 1', 'relation': 'spouse', 'verified': False, 'verification_code': False})

        response = anon.get(reverse('check_user', args=['spouse', '1', 'x']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True, 'family': 'user & spouse 1', 'relation': 'spouse', 'verified': False, 'verification_code': False})

        response = anon.get(reverse('check_user', args=['spouse', '1', user1_verification_code]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True, 'family': 'user & spouse 1', 'relation': 'spouse', 'verified': False, 'verification_code': True})

        # Create child
        response = user1.post(reverse('profile-child-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child1', 'last_name': '1'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        child1_pk = response.data['id']
        child1_verification_code = response.data['verification_code']

        response = anon.get(reverse('check_user', args=['child1', '1']))      # Newly created user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data, {'exists': True})
        self.assertEqual(response.data, {'exists': True, 'family': 'user & spouse 1', 'relation': 'child', 'verified': False, 'verification_code': False})

        #Create user for existing child profile - with correct verification
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'child1', 'last_name': '1', 'full_name': 'full name', 'verification_code': child1_verification_code})
        self.assertHttpCode(response, status.HTTP_201_CREATED)

        response = anon.get(reverse('check_user', args=['child1', '1']))      # Newly created user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data, {'exists': True})
        self.assertEqual(response.data, {'exists': True, 'verified': True})


    def test_spouse_parents(self):          # Specificaly tests if spouse parents can be edited
        # test the check_user API
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # Create spouse
        response = user1.post(reverse('profile-spouse-list', args=[self.user1.profile.pk]), format='json', data={'username': 'abx', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        spouse_pk = response.data['id']
        spouse_verification_code = response.data['verification_code']

        #Create user for existing spouse profile
        #anon = self.client
        #response = anon.post(reverse('user-create'), format='json', data={'username': 'abx_spouse', 'password': "abcdef1", 'first_name': 'spouse1', 'last_name': '1', 'full_name': 'full name', 'verification_code': spouse_verification_code})
        #self.assertHttpCode(response, status.HTTP_201_CREATED)

        # Edit spouse
        response = user1.patch(reverse('profile-spouse-detail', args=[self.user1.profile.pk, spouse_pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        # Edit spouse - direct
        response = user1.patch(reverse('profile-detail', args=[spouse_pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpCode(response, status.HTTP_200_OK)

        # Add new profile for father
        response = user1.post(reverse('profile-parent-list', args=[spouse_pk]), format='json', data={'full_name': 'fatha S1', 'dod_month': '11', 'title': 'levi', 'gender': 'm'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['full_name'], 'fatha S1')
        parent1_pk = response.data['id']
        parent_verification_code = response.data['verification_code']

        # Add new profile for mother
        response = user1.post(reverse('profile-parent-list', args=[spouse_pk]), format='json', data={'full_name': 'motha S1', 'dod_month': '10', 'title': 'levi', 'gender': 'm'})
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['full_name'], 'motha S1')
        parent2_pk = response.data['id']

        # Edit father profile
        response = user1.patch(reverse('profile-parent-detail', args=[spouse_pk, parent1_pk]), format='json', data={'full_name': 'fatha S2', 'dod_month': '9', 'title': 'levi', 'gender': 'm'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'fatha S2')
        # Edit father profile - direct
        response = user1.patch(reverse('profile-detail', args=[parent1_pk]), format='json', data={'full_name': 'fatha S3', 'dod_month': '8', 'title': 'levi', 'gender': 'm'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'fatha S3')

        # Create spouse.parent user - editing spouse and spouse-parents will now fail
        anon = self.client
        # Create with bad code
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx_parent', 'password': "abcdef1", 'first_name': 'parent1', 'last_name': '1', 'full_name': 'full name', 'verification_code': parent_verification_code+1})
        self.assertHttpError(response)
        self.assertEqual(response.data, ['Profile not found for Verification Code'])

        # Create with good code
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx_parent', 'password': "abcdef1", 'first_name': 'parent1', 'last_name': '1', 'full_name': 'full name', 'verification_code': parent_verification_code})
        self.assertHttpCode(response, status.HTTP_201_CREATED)

        # Edit father profile
        response = user1.patch(reverse('profile-parent-detail', args=[spouse_pk, parent1_pk]), format='json', data={'full_name': 'fatha S4', 'dod_month': '1', 'title': 'levi', 'gender': 'm'})
        self.assertHttpError(response)

        # Edit mother profile
        response = user1.patch(reverse('profile-parent-detail', args=[spouse_pk, parent2_pk]), format='json', data={'full_name': 'motha S2', 'dod_month': '2', 'title': 'levi', 'gender': 'm'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'motha S2')
        # Edit mother profile - direct
        response = user1.patch(reverse('profile-detail', args=[parent2_pk]), format='json', data={'full_name': 'motha S3', 'dod_month': '3', 'title': 'levi', 'gender': 'm'})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'motha S3')


        #Create user for existing spouse profile
        anon = self.client
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx_spouse', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1', 'full_name': 'full name'})
        self.assertHttpError(response)
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx_spouse', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1', 'full_name': 'full name', 'verification_code': spouse_verification_code+1})
        self.assertHttpError(response)
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx_spouse', 'password': "abcdef1", 'first_name': 'spouseXXX', 'last_name': '1', 'full_name': 'full name', 'verification_code': spouse_verification_code+1})
        self.assertHttpError(response)
        #response = anon.post(reverse('user-create'), format='json', data={'username': 'abx_spouse', 'password': "abcdef1", 'first_name': 'spouseXXX', 'last_name': '1', 'full_name': 'full name', 'verification_code': spouse_verification_code})
        #self.assertHttpError(response)
        response = anon.post(reverse('user-create'), format='json', data={'username': 'abx_spouse', 'password': "abcdef1", 'first_name': 'spouse', 'last_name': '1', 'full_name': 'full name', 'verification_code': spouse_verification_code})
        self.assertHttpCode(response, status.HTTP_201_CREATED)

        # Edit spouse
        response = user1.patch(reverse('profile-spouse-detail', args=[self.user1.profile.pk, spouse_pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpError(response)
        # Edit spouse - direct
        response = user1.patch(reverse('profile-detail', args=[spouse_pk]), format='json', data={'full_name': 'full spouse'})
        self.assertHttpError(response)
        # Edit father profile
        response = user1.patch(reverse('profile-parent-detail', args=[spouse_pk, parent1_pk]), format='json', data={'full_name': 'fatha S3', 'dod_month': '4', 'title': 'levi', 'gender': 'm'})
        self.assertHttpError(response)



    def XXtest_add_spouse2(self):
        # User1 - add new User as spouse
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertTrue(login)
        response = user1.post(reverse('user-spouse-list', args=[self.user1.pk]), format='json', data={"first_name": "spouse1", "last_name": "last1", 'username': "XXX"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        spouse1_pk = response.data['id']

        response = user1.get(reverse('user-detail', args=[spouse1_pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['verified'], False)

        response = user1.patch(reverse('user-detail', args=[spouse1_pk]), format='json', data={"full_name": "spouse fullname"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['verified'], False)

        response = user1.get(reverse('user-spouse-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.get(reverse('user-spouse-detail', args=[self.user1.pk, spouse1_pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'spouse1_last1')
        response = user1.get(reverse('user-spouse-list', args=[self.user1.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'spouse1_last1')
        response = user1.get(reverse('user-spouse-detail', args=[self.user1.pk, 99]), format='json')                # Bad spouse
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # check_user
        anon = self.client
        response = anon.get(reverse('check_user', args=['spouse1_last1']))      # Newly created user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'family': 'spouse1 last1 + user 1', 'verified': False})

        # Anon can set password for existing non-verified user
        response = anon.post(reverse('register'), format='json', data={"first_name": "spouse1", "last_name": "last1", 'password': "123456", "email": "new1@gmail.com", 'username': 'duh'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_id = response.data['id']
        self.assertEqual(new_id, spouse1_pk)
        self.assertEqual(response.data['username'], 'spouse1_last1')
        response = user1.get(reverse('user-detail', args=[spouse1_pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['verified'], True)

        spouse1 = APIClient()
        login = spouse1.login(username='spouse1_last1', password='123456')
        self.assertEqual(login, True)

        # check_user
        response = anon.get(reverse('check_user', args=['spouse1_last1']))      # Newly created user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'verified': True})





    # Also checks check_user
    def XXtest_create_user(self):
        # Anon - via user-list
        anon = self.client
        response = anon.post(reverse('user-list'), format='json', data={'username': "new_child1", 'password': "123456"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Anon - via /api/v1/auth/register/
        response = anon.get(reverse('check_user', args=['new_user1']))      # Non existing user
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = anon.post(reverse('register'), format='json', data={"first_name": "new", "last_name": "user1", 'password': ""})      # Bad Password
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = anon.post(reverse('register'), format='json', data={"first_name": "new", "last_name": "user1"})                      # Bad Password
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = anon.post(reverse('register'), format='json', data={"first_name": "new", 'password': "123456", "email": "new1@gmail.com"})       # Bad last_name
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = anon.post(reverse('register'), format='json', data={"first_name": "new", "last_name": "user1", 'password': "123456", "email": "new1@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'new_user1')
        self.assertTrue('token' in response.data)
        newuser1_id = response.data['id']
        #self.assertEqual(response.data['display_name'], '')        for some reason we don't get display_name here. is checked further on

        # check_user
        response = anon.get(reverse('check_user', args=['new_user1']))      # Newly created user
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data, {'verified': True})

        # Anon cannot set password for verified user
        response = anon.post(reverse('register'), format='json', data={"first_name": "new", "last_name": "user1", 'password': "123456", "email": "new1@gmail.com", 'username': 'duh'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # NewUser - Login
        new_user1 = APIClient()
        login = new_user1.login(username='newuser1', password='123456X')
        self.assertEqual(login, False)
        login = new_user1.login(username='new_user1', password='123456')
        self.assertEqual(login, True)
        response = new_user1.get(reverse('user-detail', args=[newuser1_id]), format='json')
        self.assertEqual(response.data['username'], 'new_user1')
        self.assertEqual(response.data['display_name'], 'new user1')

        # Anon cannot create child - Django
        response = anon.post(reverse('user-list'), format='json', data={"first_name": "first1", "last_name": "last1", 'username': "new_child13a"})                          # Anon can only add/associate user with 'register'
        self.assertHttpCode(response, status.HTTP_403_FORBIDDEN)

        # User cannot create child with user-list API, they need to use user-child-list
        response = new_user1.post(reverse('user-list'), format='json', data={"first_name": "first1", "last_name": "last2", 'username': "new_child13a", 'display_name': 'dudud'})
        self.assertHttpCode(response, status.HTTP_403_FORBIDDEN)

        #This should fail
        response = new_user1.post(reverse('user-list'), format='json', data={"first_name": "first1", "last_name": "last2", 'username': "new_child13a", 'display_name': 'dudud'})
        self.assertHttpCode(response, status.HTTP_403_FORBIDDEN)


        # even admin cannot use user-list to create new user - because it's won't be known if it's a spouse or child
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.post(reverse('user-list'), format='json', data={"first_name": "first1admin", "last_name": "last2admin", 'username': "new_child13a", 'display_name': 'dudud'})
        self.assertHttpCode(response, status.HTTP_404_NOT_FOUND)

        # admin can crete new child with user-child-list
        admin = APIClient()
        login = admin.login(username='ad_min', password='test')
        self.assertEqual(login, True)
        response = admin.post(reverse('user-child-list', args=[newuser1_id]), format='json', data={"first_name": "first1admin", "last_name": "last2admin", 'username': "new_child13a", 'display_name': 'dudud'})
        child1admin_id = response.data['id']
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'first1admin_last2admin')
        response = new_user1.get(reverse('user-child-list', args=[newuser1_id]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], child1admin_id)
        self.assertEqual(len(response.data), 1)

        self.assertHttpCode(response, status.HTTP_200_OK)
        #self.assertEqual(response.data['display_name'], 'first1admin_last2admin')
        response = admin.get(reverse('check_user', args=['first1admin_last2admin']))      # child user
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data, {'family': 'new user1', 'verified': False})
        response = anon.get(reverse('check_user', args=['first1admin_last2admin']))      # child user
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data, {'family': 'new user1', 'verified': False})

        # User can create child
        response = new_user1.post(reverse('user-child-list', args=[newuser1_id]), format='json', data={"first_name": "first1", "last_name": "last2", 'username': "new_child13a", 'display_name': 'dudud'})
        child1_id = response.data['id']
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'first1_last2')
        # Check list of children
        response = new_user1.get(reverse('user-child-list', args=[newuser1_id]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], child1_id)
        self.assertEqual(response.data[1]['id'], child1admin_id)
        self.assertEqual(len(response.data), 2)

        #self.assertEqual(response.data['display_name'], 'first1_last2')
        response = new_user1.post(reverse('user-child-list', args=[newuser1_id]), format='json', data={"first_name": "first2", "last_name": "last2", 'username': "new_child14"})      # Check that username is overwritten
        child2_id = response.data['id']
        self.assertHttpCode(response, status.HTTP_201_CREATED)
        # Check list of children
        response = new_user1.get(reverse('user-child-list', args=[newuser1_id]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], child1_id)
        self.assertEqual(response.data[1]['id'], child1admin_id)
        self.assertEqual(response.data[2]['id'], child2_id)
        self.assertEqual(len(response.data), 3)

        response = anon.get(reverse('check_user', args=['first1_last2']))      # child user
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data, {'family': 'new user1', 'verified': False})
        response = anon.get(reverse('check_user', args=['new_child14']))      # child user
        self.assertHttpCode(response, status.HTTP_404_NOT_FOUND)
        response = anon.get(reverse('check_user', args=['first2_last2']))      # child user
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data, {'family': 'new user1', 'verified': False})

        # Obtain token for new user
        new_user1_login = APIClient()
        response = new_user1_login.post(reverse('api-token-auth'), format='json', data={"first_name": "first1", "last_name": "last1", 'username': 'new_user1', 'password': "123456"})
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = new_user1_login.post(reverse('api-token-auth'), format='json', data={'username': 'new_user1', 'password': "123456"})
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = new_user1_login.post(reverse('api-token-auth'), format='json', data={'username': 'new_user1', 'password': "123456"})
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = new_user1_login.post(reverse('api-token-auth'), format='json', data={"first_name": "first2", "last_name": "last2", 'username': 'new_user1', 'password': "1"})
        self.assertHttpCode(response, status.HTTP_400_BAD_REQUEST)

        # Set Profile
        response = new_user1.get(reverse('user-detail', args=[child1_id]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['duties'], [19])         #19 is set as default

        response = admin.patch(reverse('user-detail', args=[child1_id]), format='json', data={"duties": [1]})
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = new_user1.get(reverse('user-detail', args=[child1_id]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['duties'], [1, 19])

        response = new_user1.patch(reverse('user-detail', args=[child1_id]), format='json', data={"duties": [2, 3]})
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = new_user1.get(reverse('user-detail', args=[child1_id]))
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['duties'], [2, 3, 19])

        response = new_user1.patch(reverse('user-detail', args=[self.user2.pk]), format='json', data={"duties": [2, 3]})
        self.assertHttpCode(response, status.HTTP_403_FORBIDDEN)

        #response = new_user1.put(reverse('user-child-detail', args=[newuser1_id, child1_id]), format='json', data={"yigdal": "true"})
        #self.assertHttpCode(response, status.HTTP_200_OK)


        #review the test above that still uses POST 'user-list'


    def XXtest_add_existing_spouse(self):
        spouse1 = APIClient()
        login = spouse1.login(username='user_2', password='test')
        self.assertEqual(login, True)

        # User1 - add new User as spouse
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user1.post(reverse('user-spouse-list', args=[self.user1.pk]), format='json', data={"first_name": "user", "last_name": "2", 'username': "user_2"})
        #self.user2 = User.objects.create_user(username='abc', password='test', email='user2@mail.com', first_name='user', last_name='2')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def XXtest_add_child(self):
        # User1 - add new User as child
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)
        response = user1.post(reverse('user-child-list', args=[self.user1.pk]), format='json', data={"first_name": "child1", "last_name": "last1", 'username': "XXX"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        #response = user1.post(reverse('user-child-list', args=[self.user1.pk]), format='json', data={"first_name": "child1", "last_name": "last1", 'username': "XXX"})
        #self.assertEqual(response.status_code, status.HTTP_200_OK)          #trying to add same username returns 200
        child1_pk = response.data['id']


        response = user1.get(reverse('user-detail', args=[child1_pk]), format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['verified'], False)

        response = user1.get(reverse('user-child-detail', args=[self.user1.pk, self.user3.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = user1.get(reverse('user-child-detail', args=[self.user1.pk, child1_pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'child1_last1')
        response = user1.get(reverse('user-child-list', args=[self.user1.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], 'child1_last1')
        response = user1.get(reverse('user-child-detail', args=[self.user1.pk, 99]), format='json')                # Bad child
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # check_user
        anon = self.client
        response = anon.get(reverse('check_user', args=['child1_last1']))      # Newly created user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'family': 'user 1', 'verified': False})

        # Anon can set password for existing non-verified user
        response = anon.post(reverse('register'), format='json', data={"first_name": "child1", "last_name": "last1", 'password': "123456", "email": "new1@gmail.com", 'username': 'duh'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_id = response.data['id']
        self.assertEqual(new_id, child1_pk)
        self.assertEqual(response.data['username'], 'child1_last1')
        response = user1.get(reverse('user-detail', args=[child1_pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['verified'], True)

        child1 = APIClient()
        login = child1.login(username='child1_last1', password='123456')
        self.assertEqual(login, True)

        # check_user
        response = anon.get(reverse('check_user', args=['child1_last1']))      # Newly created user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'verified': True})

    def XXtest_parent_name_flat(self):
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        #Add full_name
        response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        self.assertEqual(response.data['full_name'], "")
        response = user1.patch(reverse('user-detail', args=[self.user1.pk]), format='json', data={"full_name": "פלוניא"})
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא")
        print(response.data)

        #Add father full_name
        response = user1.patch(reverse('user-detail', args=[self.user1.pk]), format='json', data={"father": {"full_name": "פלוניב בן פלוניג"}})
        self.assertHttpCode(response, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא בן פלוניב")
        self.assertEqual(response.data['father']['full_name'], "פלוניב בן פלוניג")
        #self.assertEqual(response.data['father']['full_aliya_name'], "פלוניב בן פלוניג")
        response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['father']['full_name'], "פלוניב בן פלוניג")
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא בן פלוניב")

        #Set user-type on son
        response = user1.patch(reverse('user-detail', args=[self.user1.pk]), format='json', data={"user_type": "cohen"})
        self.assertHttpCode(response, status.HTTP_200_OK)
        response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['user_type'], "cohen")
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא בן פלוניב הכהן")

        #Set user-type on parent
        #response = user1.patch(reverse('user-detail', args=[self.user1.pk]), format='json', data={"father": {"user_type": "levi"}})
        #self.assertHttpCode(response, status.HTTP_200_OK)
        #response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        #self.assertHttpCode(response, status.HTTP_200_OK)
        #self.assertEqual(response.data['user_type'], "cohen")
        #self.assertEqual(response.data['full_aliya_name'], "פלוניא בן פלוניב הכהן")
        #self.assertEqual(response.data['father']['user_type'], "levi")
        #self.assertEqual(response.data['father']['full_aliya_name'], "פלוניב בן פלוניג הלוי")



        #Add mother full_name
        response = user1.patch(reverse('user-detail', args=[self.user1.pk]), format='json', data={"mother": {"full_name": "פלוניתב בת פלוניתג"}})
        self.assertHttpCode(response, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא בן פלוניב הכהן")
        self.assertEqual(response.data['father']['full_name'], "פלוניב בן פלוניג")
        self.assertEqual(response.data['mother']['full_name'], "פלוניתב בת פלוניתג")
        #self.assertEqual(response.data['father']['full_aliya_name'], "פלוניב בן פלוניג")
        response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['father']['full_name'], "פלוניב בן פלוניג")
        self.assertEqual(response.data['mother']['full_name'], "פלוניתב בת פלוניתג")
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא בן פלוניב הכהן")



    def XXtest_parent_name_user(self):
        user1 = APIClient()
        login = user1.login(username='user_1', password='test')
        self.assertEqual(login, True)

        # User1 - add new User as child
        response = user1.post(reverse('user-child-list', args=[self.user1.pk]), format='json', data={"first_name": "child1", "last_name": "last1", 'username': "XXX"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        child1_pk = response.data['id']

        # Add full_name
        response = user1.patch(reverse('user-detail', args=[self.user1.pk]), format='json', data={"full_name": "פלוניא"})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'פלוניא')

        # Check parent
        response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא")
        print('father: ', response.data)

        # Check child
        response = user1.get(reverse('user-detail', args=[child1_pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['father']['full_name'], 'פלוניא')

        # Verify child
        anon = self.client
        response = anon.post(reverse('register'), format='json', data={"first_name": "child1", "last_name": "last1", 'password': "123456", "email": "new1@gmail.com", 'username': 'duh'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        child1 = APIClient()
        login = child1.login(username='child1_last1', password='123456')
        self.assertEqual(login, True)

        #Add grandfather full_name
        response = user1.patch(reverse('user-detail', args=[self.user1.pk]), format='json', data={"father": {"full_name": "פלוניב בן פלוניג"}})
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא בן פלוניב")
        self.assertEqual(response.data['father']['full_name'], "פלוניב בן פלוניג")
        #self.assertEqual(response.data['father']['full_aliya_name'], "פלוניב בן פלוניג")
        response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        self.assertHttpCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['father']['full_name'], "פלוניב בן פלוניג")
        response = user1.get(reverse('user-detail', args=[self.user1.pk]), format='json')
        self.assertEqual(response.data['full_name'], "פלוניא")
        self.assertEqual(response.data['full_aliya_name'], "פלוניא בן פלוניב")
        self.assertEqual(response.data['father']['full_name'], "פלוניב בן פלוניג")
