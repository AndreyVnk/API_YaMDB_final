from datetime import datetime

from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(validators=[
        UniqueValidator(queryset=Category.objects.all()),
        RegexValidator(regex='^[-a-zA-Z0-9_]+$')
    ])

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(validators=[
        UniqueValidator(queryset=Genre.objects.all()),
        RegexValidator(regex='^[-a-zA-Z0-9_]+$')
    ])

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(read_only=True, )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, title):
        rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        if rating.get('score__avg') is None:
            return None
        return int(rating.get('score__avg'))


class CreateUpdateTitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        read_only=False,
        queryset=Genre.objects.all(),
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Ошибка. Год создания произведения еще не наступил'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title_id = (
            self.context["request"].parser_context["kwargs"].get("title_id"))
        author = self.context["request"].user
        current_title = get_object_or_404(Title, id=title_id)
        if self.context["request"].method == "POST" and (
           current_title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(
                "Review on this title already exists.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def update(self, instance, validated_data):
        if validated_data.get('role') is not None:
            validated_data.pop('role')
        return super().update(instance, validated_data)


class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {"Wrong username": "User 'me' can not be created."}
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']

    def validate_username(self, value):
        try:
            CustomUser.objects.filter(username=value).exists()
        except CustomUser.DoesNotExist:
            raise Http404
        else:
            return value

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(CustomUser, username=username)
        if not user:
            raise serializers.ValidationError({
                "Wrong username or confirmation code":
                    "Please input correct data."
            })
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError({
                'confirmation_code': ['Invalid value']})
        return data
