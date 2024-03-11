from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class AuthUser(AbstractUser):
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=50)
    
    class Meta: 
        managed = True
        db_table = "Usee"
        unique_together = ('username',)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs): 
        return super().save(*args, **kwargs)