from django.db import models
from category.models import Category
from django.contrib.auth import get_user_model


User = get_user_model()


class Movie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='cinema')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='cinema', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ['owner', 'movie']


class Favorites(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['owner', 'movie']
