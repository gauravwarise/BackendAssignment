from itertools import chain
from collections import Counter
from itertools import islice
from django.db.models import Prefetch
from apps.movies.models import Movies

class TopFavouriteGenres(object):
    @staticmethod
    def top_n_genres(lst, n=3):
        return ",".join(genre for genre, _ in Counter(lst).most_common(n))

    def top_favourite_genres(self, collections, n=3):
        genres_list = list(chain.from_iterable(
            movie.genres.split(",") for collection in collections.prefetch_related(
                Prefetch("movies", queryset=Movies.objects.only("genres"), to_attr="genres_movies")
            ) for movie in collection.genres_movies
        ))
        return self.top_n_genres(genres_list, n)
  