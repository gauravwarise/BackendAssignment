from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.status import *
from rest_framework import status
from apps.utils.get_movies import GetMovies
from .serializers import *
from django.core.cache import cache
from django.core.exceptions import *
from django.db.models import Prefetch, Count
from apps.utils.movie_helper import TopFavouriteGenres

# Create your views here.



class MovieView(APIView):
    permission_classes = (AllowAny,)
    def get(self,request):
        response = {"status": "success", "data": "", "message":"", "http_status": HTTP_201_CREATED}
        try:
            url = "https://demo.credy.in/api/v1/maya/movies/"
            username = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
            password = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"

            movie_list = GetMovies.getMovies(url, username, password)
            if movie_list:
                response["data"] = movie_list
                print(movie_list)
            else:
                response["message"] = "data not found!!"
            return JsonResponse(response)
        except Exception as e:
            print(e)
        return JsonResponse(response)



class CollectionView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        response = {"status": "success", "data": "", "message":"", "http_status": HTTP_201_CREATED}
        print(request.data)
        data = request.data
        collection = Collection.objects.create(
            title=data["title"], description=data["description"], user=request.user
        )  
        collection.save()
        for movie in data["movies"]:
            if Movies.objects.filter(uuid=movie["uuid"]).exists():
                movie_obj = Movies.objects.get(uuid=movie["uuid"])
            else:
                movie_obj = Movies.objects.create(
                    uuid=movie["uuid"],
                    title=movie["title"],
                    description=movie["description"],
                    genres=movie["genres"],
                )

            collection.movies.add(movie_obj)

        serializer = CollectionSerializer(collection)
        context = {"collection_uuid": serializer.data["uuid"]}
        return JsonResponse(context, status=status.HTTP_201_CREATED)
        
    
    def get_object(self, uuid):
        try:
            print(uuid,"=====================",Collection.objects.get(uuid=uuid))
            return Collection.objects.get(uuid=uuid)
        except ValidationError:
            return JsonResponse({"error": "Invalid UUID format."}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, uuid=None):
        response = {"status": "success", "data": "", "message":"", "http_status": HTTP_201_CREATED}
        if uuid == None:
            collections = Collection.objects.filter(user=request.user)
            serializer = GetCollectionSerializer(collections, many=True)

            collection_list = {"collection": serializer.data}
            favourite_genres = (
                TopFavouriteGenres().top_favourite_genres_from_user_movie_collection(
                    collections, n=3
                )
            )

            context = {
                "is_success": True,
                "data": collection_list,
                "favourite_genres": favourite_genres,
            }
            return JsonResponse(context, status=status.HTTP_200_OK)
            # collections = (
            #     Collection.objects.filter(user=request.user)
            #     .prefetch_related(
            #         Prefetch(
            #             "movies",
            #             queryset=Movies.objects.all()
            #         )
            #     )
            # )

            # movies_in_collections = [collection.movies.all() for collection in collections]
            # all_movies = [movie for sublist in movies_in_collections for movie in sublist]

            # genre_counts = {}
            # for movie in all_movies:
            #     genres = movie.genres.split(",")
            #     for genre in genres:
            #         genre_counts[genre.strip()] = genre_counts.get(genre.strip(), 0) + 1

            # sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            # favourite_genres = ", ".join([genre[0] for genre in sorted_genres])

            # response_data = {
            #     "collections": [
            #         {
            #             "title": collection.title,
            #             "uuid": str(collection.uuid),
            #             "description": collection.description
            #         }
            #         for collection in collections
            #     ],
            #     "favourite_genres": favourite_genres
            # }

            # return JsonResponse({"is_success": True, "data": response_data})
            # collections = Collection.objects.filter(user=request.user)
            # serializer = GetCollectionSerializer(collections, many=True)
            # collection_list = {"collection": serializer.data}
            # context = {
            #     "is_success": True,
            #     "data": collection_list,
            #     # "favourite_genres": favourite_genres,
            # }
            # return JsonResponse(context, status=status.HTTP_200_OK)
        else:
            
            try:
                collection = self.get_object(uuid)
                serializer = CollectionSerializer(collection)
                try:
                    movie_queryset = collection.movies.all()
                except Exception as e:
                    context = {"error": "Invalid uuid."}
                    return JsonResponse(context)
                movies_data = MovieSerializer(movie_queryset, many=True).data
                context = {
                    "title": serializer.data["title"],
                    "description": serializer.data["description"],
                    "movies": movies_data,
                }
            except ObjectDoesNotExist:
                context = {"error": "Collection not found."}
            return JsonResponse(context)


    
    def put(self, request, uuid, format=None):
        instance = self.get_object(uuid)

        if "movies" in request.data:
            movies = request.data.pop("movies")
            for movie in movies:
                movie_instance = Movies.objects.get(uuid=movie["uuid"])
                movie_serializer = MovieSerializer(
                    movie_instance, data=movie, partial=True
                )
                movie_serializer.is_valid(raise_exception=True)
                movie_serializer.save()

        serializer = CollectionSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return JsonResponse({"details": "updated"})
    
    def delete(self, request, uuid, format=None):
        try:
            # instance = self.get_object(uuid)
            instance = Collection.objects.get(uuid=uuid)
            print(instance, "<=======================")
            instance.delete()
            return JsonResponse({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)





        #     return JsonResponse({"detail": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        # except ObjectDoesNotExist:
        #     return JsonResponse({"error": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)



class RequestCount(APIView):
    def get(self, request, *args, **kwargs):
        request_count = cache.get("request_count")
        context = {"requests": request_count}
        return JsonResponse(context, status=status.HTTP_200_OK)


class RequestCountRest(APIView):
    def post(self, request, *args, **kwargs):
        cache.set("request_count", 0)
        context = {"message": "request count reset successfully"}
        return JsonResponse(context, status=status.HTTP_200_OK)
