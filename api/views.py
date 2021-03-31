from rest_framework import status, permissions, viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken


from .pagination import CursorPagination
from .filters import TitleFilter
from .models import CustomUser, Category, Genre, Title
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import( 
    RegistrationSerializer, LoginSerializer, UserSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer
)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data,
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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter       
    pagination_class = CursorPagination
