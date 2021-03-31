from rest_framework import serializers
from .models import CustomUser, Category, Genre, Title
from django.contrib.auth.tokens import default_token_generator
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id', ]
        

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre        
        exclude = ['id', ]


class GenreField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return GenreSerializer(value).data


class CategoryField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return CategorySerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

