from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(
        _('Имя категории'), max_length=256, blank=False)
    slug = models.SlugField(
        _('Slug категории'), unique=True, max_length=50, blank=False)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        _('Имя жанра'), max_length=256, blank=False)
    slug = models.SlugField(
        _('Slug жанра'), unique=True)

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(_('Название'), max_length=200, blank=False)
    year = models.IntegerField(_('Год выпуска'), blank=False)
    description = models.CharField(_('Описание'), max_length=200)
    rating = models.IntegerField(_('Рейтинг'), null=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, blank=False)

    class Meta:
        verbose_name = _('Произведение')
        verbose_name_plural = _('Произведения')


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Жанр-произведение')
        verbose_name_plural = _('Жанры-произведения')


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name=_('Произведение'),
        related_name='reviews'
    )
    text = models.TextField(_('Текст отзыва'), blank=False)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Автор отзыва'),
    )
    score = models.IntegerField(
        _('Оценка'),
        blank=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        _('Дата добавления'), auto_now_add=True
    )

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Автор комментария')
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name=_('Отзыв')
    )
    text = models.TextField(_('Текст комментария'), blank=False)
    pub_date = models.DateTimeField(
        _('Дата добавления'), auto_now_add=True
    )

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
        ordering = ['-pub_date']
