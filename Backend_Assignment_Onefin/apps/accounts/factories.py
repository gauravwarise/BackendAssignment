from factory.django import DjangoModelFactory
from factory import Sequence
from django.contrib.auth.hashers import make_password
from .models import AuthUser

class AuthUserFactory(DjangoModelFactory):
    class Meta:
        model = AuthUser

    username = Sequence(lambda n: f'user{n}')
    password = make_password('password123')  



# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = AuthUser

#     username = factory.Faker('user_name')
#     password = factory.Faker('password')

#     @classmethod
#     def create(cls, **kwargs):
#         user = super().create(**kwargs)
#         # Generate JWT token for the user
#         refresh_token = RefreshToken.for_user (user)
#         user.access_token = str(refresh_token.access_token)
#         return user