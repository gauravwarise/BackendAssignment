# from django.test import TestCase

# # Create your tests here.
# import pytest
# from .factories import UserFactory, CollectionFactory, MovieFactory

# # this test is not completed
# class TestGetCollection(object):
#     @pytest.mark.tcid31
#     @pytest.mark.django_db
#     def test_get_collection_api(self):
#         # Create a user instance
#         user_instance = UserFactory()

#         # Create a collection instance associated with the user
#         collection_instance = CollectionFactory(user=user_instance)

#         assert True



from django.test import TestCase
from apps.movies.models import Movies, Collection
from apps.movies.factories import MoviesFactory, CollectionFactory

class MoviesModelTest(TestCase):
    def test_movie_creation(self):
        movie = MoviesFactory()
        self.assertEqual(movie.title, 'Test Movie')
        self.assertEqual(movie.description, 'This is a test movie')
        self.assertEqual(movie.genres, 'Action')
        self.assertIsNotNone(movie.uuid)

class CollectionModelTest(TestCase):
    def test_collection_creation(self):
        movie1 = MoviesFactory()
        movie2 = MoviesFactory()

        collection = CollectionFactory(movies=[movie1, movie2])

        self.assertEqual(collection.title, 'Test Collection')
        self.assertEqual(collection.description, 'This is a test collection')
        self.assertIsNotNone(collection.user)
        self.assertEqual(collection.movies.count(), 2)
