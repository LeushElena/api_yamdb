from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mail


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def create(self, validated_data):
        user = CustomUser(email=validated_data['email'])
        confirmation_code = default_token_generator.make_token(user)
        user = CustomUser(email=validated_data['email'], confirmation_code=confirmation_code)
        user.save()
        send_mail(
            'Confirmation_code',
            confirmation_code,
            'admin@yambdb.com',
            [validated_data['email']],
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role',)