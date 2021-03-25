from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mail

class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.CharField(
        max_length=255,
        min_length=5,
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def create(self):
        CustomUser.objects.create(email=self.email, password=self.email)
        user = get_object_or_404(CustomUser, email=self.email)
        confirmation_code = default_token_generator.make_token(user)
        CustomUser.objects.update(confirmation_code = confirmation_code)
        return user
