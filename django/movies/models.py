from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('Genre'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        db_table = "content\".\"genre"

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('Full name'), max_length=255)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        db_table = "content\".\"person"

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeFilmwork(models.TextChoices):
        MOVIE = 'M', _('Movie')
        TV_SHOW = 'T', _('TV Show')

    title = models.CharField(_('Movie title'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    creation_date = models.DateField(_('Release Date'), blank=True, null=True)
    certificate = models.TextField(_('Certificate'), null=True, blank=True)
    type = models.CharField(_('Type'), choices=TypeFilmwork.choices, max_length=1)
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmwork')
    rating = models.FloatField(_('Rating'), blank=True, null=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    file_path = models.FileField(_('File'), blank=True, null=True, upload_to='movies/')

    class Meta:
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
        db_table = "content\".\"film_work"

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Movie genre')
        verbose_name_plural = _('Movie genres')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'],
                name='unique_film_work_genre',
            ),
        ]
        db_table = "content\".\"genre_film_work"


class RoleType(models.TextChoices):
    ACTOR = 'A', _('Actor')
    WRITER = 'W', _('Writer')
    DIRECTOR = 'D', _('Director')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('Role'), null=True, max_length=1, choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Role of the person')
        verbose_name_plural = _('Roles of Persons')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='unique_film_work_person',
            ),
        ]
        db_table = "content\".\"person_film_work"