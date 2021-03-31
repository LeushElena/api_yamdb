from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    AuthTokenJwt,
    RegistrationAPIView,
    UserViewSet,
    UserMeViewSet,
)
router_v1 = DefaultRouter()
#router_v1.register('users/me', UserMeViewSet, basename='user_me')
router_v1.register(r'users', UserViewSet, basename='users')
urlpatterns = [
    path('v1/auth/token/', AuthTokenJwt),
    path('v1/auth/email/', RegistrationAPIView.as_view()),
    path('v1/users/me/', UserMeViewSet.as_view()),
    path('v1/', include(router_v1.urls)),
]