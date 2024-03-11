from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Movies, Collection


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ["uuid", "title", "description", "genres"]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["uuid", "title", "description", "user", "movies"]


class GetCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["uuid", "title", "description"]
