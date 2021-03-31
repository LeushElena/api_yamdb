from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers

from .models import Category, Comment, CustomUser, Genre, Review, Title


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
        

class TitleRatingSerialier(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only = ['id', 'author', 'pub_date']

    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if (self.context['request'].method == 'POST'
            and Review.objects.filter(author=user,
                                      title_id=title_id).exists()):
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only = ['id', 'author', 'pub_date']