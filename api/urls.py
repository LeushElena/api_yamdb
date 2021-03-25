from django.urls import include, path

from .views import RegistrationAPIView
#from .views import LoginAPIView

urlpatterns = [
    path('v1/auth/email/', RegistrationAPIView.as_view(), name='user_registration'),
    #path('v1/token/', LoginAPIView.as_view(), name='user_login'),
]