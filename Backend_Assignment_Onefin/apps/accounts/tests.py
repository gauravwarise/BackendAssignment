from rest_framework.test import APITestCase
from rest_framework import status
from .factories import AuthUserFactory
from .models import AuthUser

class UserRegistrationViewTestCase(APITestCase):
    def test_user_registration_success(self):
        data = {
            'username': 'test_user',
            'password': 'Password@.123'
        }

        response = self.client.post('/register', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_count = AuthUser.objects.filter(username='test_user').count()
        self.assertEqual(user_count, 1)

    def test_user_registration_failure(self):
        data = {
            'username': 'existing_user',
            'password': 'password123'
        }

        # Create an existing user
        AuthUserFactory(username='existing_user')

        response = self.client.post('/register', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# import pytest

# @pytest.mark.customers
# class TestUserRegistration(object):

#     @pytest.mark.tcid29
#     @pytest.mark.django_db
#     def test_user_registration_success(self, user):

#         # check user generated
#         assert user is not None, "User not created successfully"

#         # Check if the access_token is generated
#         assert user.access_token, "Access token not generated"

