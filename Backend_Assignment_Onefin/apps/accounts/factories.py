from factory.django import DjangoModelFactory
from factory import Sequence
from django.contrib.auth.hashers import make_password
from .models import AuthUser

class AuthUserFactory(DjangoModelFactory):
    class Meta:
        model = AuthUser

    username = Sequence(lambda n: f'user{n}')
    password = make_password('password123')  

