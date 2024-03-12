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
            return

        if extracted:
            for movie in extracted:
                self.movies.add(movie)
