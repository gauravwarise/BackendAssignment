from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.status import *
from rest_framework import status
from apps.utils.get_movies import GetMovies
from .serializers import *
from django.core.cache import cache
from django.core.exceptions import *
from apps.utils.movie_helper import TopFavouriteGenres

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    def get(self,request):
        context = dict()
        try:
            url = "https://demo.credy.in/api/v1/maya/movies/"
            username = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
            password = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"

            movie_list = GetMovies.getMovies(url, username, password)
            if movie_list:
                context["data"] = movie_list
                print(movie_list)
            else:
                context["message"] = "data not found!!"
            return JsonResponse(context)
        except Exception as e:
            print(e)
        return JsonResponse(context)



class CollectionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    def post(self, request):
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
        context = {"collection_uuid":serializer.data["uuid"]}
        return JsonResponse(context, status=status.HTTP_200_OK)
        
    
    def get_object(self, uuid):
        try:
            return Collection.objects.get(uuid=uuid)
        except ValidationError:
            return JsonResponse({"error": "Invalid UUID format."}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, uuid=None):
        if uuid == None:
            collections = Collection.objects.filter(user=request.user)
            serializer = GetCollectionSerializer(collections, many=True)

            collection_list = {"collection": serializer.data}
            favourite_genres = (
                TopFavouriteGenres().top_favourite_genres(
                    collections, n=3
                )
            )
            context = {
                "is_success": True,
                "data": collection_list,
                "favourite_genres": favourite_genres,
            }
            return JsonResponse(context, status=status.HTTP_200_OK)
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
                return JsonResponse(context, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Collection not found."},status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, uuid):
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
        if serializer.is_valid:
            serializer.is_valid(raise_exception=True)
            serializer.save() 
            return JsonResponse({"details": "Update successfull."}, status=status.HTTP_200_OK)
        else: 
            return JsonResponse({"details": "Failed to update."}, status=status.HTTP_409_CONFLICT)
    
    def delete(self, request, uuid, format=None):
        try:
            instance = Collection.objects.get(uuid=uuid)
            instance.delete()
            return JsonResponse({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)

class RequestCount(APIView):
    def get(self, request, *args, **kwargs):
        request_count = cache.get("request_count")
        context = {"requests": request_count}
        return JsonResponse(context, status=status.HTTP_200_OK)

class RequestCountRest(APIView):
    def get(self, request, *args, **kwargs):
        cache.set("request_count", 0)
        context = {"message": "request count reset successfully"}
        return JsonResponse(context, status=status.HTTP_200_OK)
