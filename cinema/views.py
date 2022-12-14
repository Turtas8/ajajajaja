from django.shortcuts import render
from rest_framework import permissions, response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from . import serializers
from .models import Movie
from .permissions import IsAuthor
from rating.serializers import ReviewSerializer
# from comment.serializers import CommentSerializer
from rest_framework.response import Response
from .models import Like, Favorites
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .service import MovieFilter


class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 1000


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_class = MovieFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        elif self.action in ('create', 'add_to_liked', 'remove_from_liked', 'favorite_action'):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # api/v1/movies/<id>/reviews/
    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk):
        product = self.get_object()
        if request.method == 'GET':
            reviews = product.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return response.Response(serializer.data, status=200)
        if product.reviews.filter(owner=request.user).exists():
            return response.Response('???? ?????? ?????????????????? ??????????!!', status=400)
        data = request.data
        serializer = ReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, product=product)
        return response.Response(serializer.data, status=201)

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        movie = self.get_object()
        user = request.user
        if user.liked.filter(movie=movie).exists():
            return Response('This Movie is Already Liked!', status=400)
        Like.objects.create(owner=user, movie=movie)
        return Response('You Liked The Movie', status=201)

    # /posts/<id>?remove_from_liked/
    @action(['DELETE'], detail=True)
    def remove_from_liked(self, request, pk):
        movie = self.get_object()
        user = request.user
        if not user.liked.filter(movie=movie).exists():
            return Response('You Didn\'t Like This Movie!', status=400)
        user.liked.filter(movie=movie).delete()
        return Response('Your Like is Deleted!', status=204)

    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        movie = self.get_object()
        likes = movie.likes.all()
        serializer = serializers.LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def favorite_action(self, request, pk):
        movie = self.get_object()
        user = request.user
        if user.favorites.filter(movie=movie).exists():
            user.favorites.filter(movie=movie).delete()
            return Response('Deleted From Favorites!', status=204)
        Favorites.objects.create(owner=user, movie=movie)
        return Response('Added to Favorites!', status=201)

    @action(['DELETE'], detail=True)
    def remove_from_favorites(self, request, pk):
        movie = self.get_object()
        user = request.user
        if not user.favorites.filter(movie=movie).exists():
            return Response('This Movie is not in Favorites!', status=400)
        user.favorites.filter(movie=movie).delete()
        return Response('Your Favorite is Deleted!', status=204)

    @action(['GET'], detail=True)
    def get_favorites(self, request, pk):
        movie = self.get_object()
        favorites = movie.favorites.all()
        serializer = serializers.FavoritesSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(['DELETE'], detail=True)
    def remove_from_reviews(self, request, pk):
        movie = self.get_object()
        user = request.user
        if not user.review.filter(movie=movie).exists():
            return Response('You are not Review This Movie!', status=400)
        user.review.filter(movie=movie).delete()
        return Response('Your Review is Deleted!', status=204)


def auth(request):
    return render(request, 'oauth.html')
