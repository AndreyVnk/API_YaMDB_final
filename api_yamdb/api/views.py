from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser
from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    IsAdminOrModerator,
    IsOwnerOrReadOnly,
    ReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CreateCustomUserSerializer,
    CreateUpdateTitleSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer,
)


class BaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)

    def get_permissions(self):
        if self.action == "list":
            return (ReadOnly(),)
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == "destroy":
            return (IsAdminOrModerator(),)
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def get_permissions(self):
        if self.action == "destroy":
            return (IsAdminOrModerator(),)
        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    search_fields = ("name",)


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return CreateUpdateTitleSerializer
        return TitleSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        methods=["patch", "get"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
        url_name="users_me",
    )
    def me(self, request, *args, **kwargs):
        user_instance = self.request.user
        serializer = self.get_serializer(user_instance)
        if self.request.method == "PATCH":
            serializer = self.get_serializer(
                data=request.data, instance=user_instance, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class EmailConfirmationViewSet(CreateModelMixin, GenericAPIView):
    serializer_class = CreateCustomUserSerializer

    def post(self, request):
        serializer = CreateCustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            CustomUser, username=serializer.validated_data.get("username")
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            "Hello",
            f"This is your confirmation code: {confirmation_code}",
            settings.EMAIL_FROM,
            [serializer.validated_data.get("email")],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewAPI(GenericAPIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser, username=serializer.validated_data["username"]
        )
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_201_CREATED)
