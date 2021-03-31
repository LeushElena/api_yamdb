from rest_framework import status, filters, permissions, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdmin
from .pagination import CursorPagination

from .models import CustomUser
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer

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
