from django.db import models
import uuid
from apps.accounts.models import AuthUser
# Create your models here.



class Movies(models.Model):

    title = models.CharField(max_length=300)
    description = models.TextField()
    genres = models.CharField(max_length=225)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.title


class Collection(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="collections")
    movies = models.ManyToManyField(Movies, related_name="collections")

    def __str__(self):
        return self.title
