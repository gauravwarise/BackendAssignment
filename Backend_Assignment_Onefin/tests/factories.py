import factory

from apps.accounts.models import AuthUser


class AuthUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AuthUser
    name = "test_authuser" 