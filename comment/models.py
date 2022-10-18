from django.db import models
from django.contrib.auth import get_user_model
from cinema.models import Movie


User = get_user_model()


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.movie} -> {self.created_at}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'