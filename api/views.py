from django.db.models.aggregates import Avg
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, CustomUser, Genre, Review, Title
from .pagination import CursorPagination
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, LoginSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleRatingSerialier, TitleSerializer,
                          UserSerializer)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def AuthTokenJwt(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = CustomUser.objects.get(
            email=email,
            confirmation_code=confirmation_code,
        )
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'token': token})
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    pagination_class = CursorPagination


class UserMeViewSet(APIView):
    def get(self, request):
        user = CustomUser.objects.get(pk=self.request.user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = CustomUser.objects.get(pk=self.request.user.pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    pagination_class = CursorPagination
    search_fields = ('=name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    pagination_class = CursorPagination
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    pagination_class = CursorPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleRatingSerialier
        else:
            return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly]
    pagination_class = CursorPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        params = {
            'author': self.request.user,
            'title_id': self.kwargs.get('title_id')
        }
        get_object_or_404(Title, id=params['title_id'])
        serializer.save(**params)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly]
    pagination_class = CursorPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        params = {
            'author': self.request.user,
            'review_id': self.kwargs.get('review_id')
        }
        get_object_or_404(Review, id=params['review_id'])
        serializer.save(**params)
