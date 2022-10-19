from django.contrib import admin
from cinema.models import Movie, Like, Favorites


admin.site.register(Movie)
admin.site.register(Like)
admin.site.register(Favorites)
