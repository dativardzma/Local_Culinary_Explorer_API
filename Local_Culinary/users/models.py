from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUser(AbstractUser):
    roles = [
                ('customer', 'Customer'),
                ('worker', 'Worker')
            ]
    role = models.CharField(max_length=50, choices=roles, blank=True, null=True)
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'acsses': str(refresh.access_token)}

    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

class Dish_Images(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=200)
    categories = [
        ('meal', 'Meal'),
        ('desert', 'Desert')
    ]
    category = models.CharField(max_length=50, choices=categories, blank=True, null=True)
    ingredients = models.TextField(max_length=500)
    photo = models.ManyToManyField(Dish_Images)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
