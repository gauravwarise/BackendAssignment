from pytest_factoryboy import register


from .factories import AuthUserFactory
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend_Assignment_Onefin.settings")

import django
django.setup()


register(AuthUserFactory)