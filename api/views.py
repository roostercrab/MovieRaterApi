from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            print(f'This is the primary key: {pk}')
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                message_to_user = {
                    "message": "Rating updated",
                    "result": serializer.data,
                }
                return Response(message_to_user, status=status.HTTP_200_OK)

            except:
                Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                message_to_user = {
                    "message": "Rating created",
                    "result": serializer.data,
                }
                return Response(message_to_user, status=status.HTTP_200_OK)

        else:
            message_to_user = {'message': 'there are no stars here'}
            return Response(message_to_user, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
