from django.test import TestCase
from apps.movies.factories import MoviesFactory, CollectionFactory
from apps.accounts.factories import AuthUserFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


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
    
    def setUp(self):
        self.user = AuthUserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.collection = CollectionFactory(user=self.user)

    def test_get_collection_list(self):
        url = reverse('collection')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['is_success'], True)

    def test_get_single_collection(self):
        url = reverse('collection-details', args=[str(self.collection.uuid)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], self.collection.title)
        self.assertEqual(response.json()['description'], self.collection.description)

    