from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import get_object_or_404

class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.CharField(
        max_length=255,
        min_length=5,
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def create(self, validated_data):
        user = get_object_or_404(CustomUser, email=email)
        confirmation_code = default_token_generator.make_token(user)
        CustomUser.objects.create(confirmation_code = confirmation_code, **validated_data)
        return send_mail(
            'Subject here',
            'Here is the message.',
            user.confirmation_code,
            user.email,
            fail_silently=False,
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    confirmation_code = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        confirmation_code = data.get('confirmation_code', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if confirmation_code is None:
            raise serializers.ValidationError(
                'A confirmation_code is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }