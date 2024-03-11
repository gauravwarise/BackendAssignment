# import factory
# import uuid
# from .models import *
# from apps.accounts.factories import UserFactory

# class MovieFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Movies

#     # Define movie fields with either static or dynamic data

#     uuid = uuid.uuid4()  # You can set a specific UUID or use the default one
#     title = factory.Faker('sentence')
#     description = factory.Faker('text')
#     genres = factory.Faker('word')


# class CollectionFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Collection

#     # Define collection fields with either static or dynamic data
#     uuid = uuid.uuid4()
#     title = factory.Faker ('sentence')
#     description = factory.Faker ('text')
#     user = factory.SubFactory(UserFactory)
#     movies = factory.SubFactory(MovieFactory)


import factory
from factory.django import DjangoModelFactory
from .models import Movies, Collection
# from django.contrib.auth.models import User
from apps.accounts.models import AuthUser

class UserFactory(DjangoModelFactory):
    class Meta:
        model = AuthUser

    username = factory.Sequence(lambda n: 'user_%d' % n)

class MoviesFactory(DjangoModelFactory):
    class Meta:
        model = Movies

    title = 'Test Movie'
    description = 'This is a test movie'
    genres = 'Action'

class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    title = 'Test Collection'
    description = 'This is a test collection'
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def movies(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of movies were passed in, use them
            for movie in extracted:
                self.movies.add(movie)
