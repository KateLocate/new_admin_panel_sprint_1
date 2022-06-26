"""Models structure for movies app."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from movies.models_choices import FilmworkType, Gender, PersonRole


class TimeStampedMixin(models.Model):
    """Represents basic time attributes for creating and updating entries."""

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        """Meta information on TimeStampedMixin."""

        abstract = True


class UUIDMixin(models.Model):
    """Represents id attribute containing UUID for creating entries."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Meta information on UUIDMixin."""

        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Stores a single genre entry."""

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        """Meta information on :model:`movies.Genre`."""

        db_table = '"content"."genre"'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        """Verbose representation of Genre entry."""
        return self.name


class GenreFilmwork(UUIDMixin):
    """Stores a single filmwork genre entry,
    related to :model:`movies.Filmwork` and :model:`movies.Genre`.
    """

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        """Meta information on :model:`movies.GenreFilmwork`."""

        db_table = '"content"."genre_film_work"'
        verbose_name = _('Film Genre')
        verbose_name_plural = _('Film Genres')

        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='film_work_genre'),
        ]
        indexes = [
            models.Index(fields=['film_work', 'genre']),
        ]

    def __str__(self):
        """Verbose representation of GenreFilmwork entry."""
        return self.genre.name


class Person(UUIDMixin, TimeStampedMixin):
    """Stores a single person entry."""

    full_name = models.TextField(_('full_name'))
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        """Meta information on :model:`movies.Person`."""

        db_table = '"content"."person"'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        """Verbose representation of Person entry."""
        return self.full_name


class PersonFilmwork(UUIDMixin):
    """Stores a single filmwork person entry,
    related to :model:`movies.Filmwork` and :model:`movies.Person`.
    """

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('role'), choices=PersonRole.choices, max_length=15, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta information on :model:`movies.PersonFilmwork`."""

        db_table = '"content"."person_film_work"'
        verbose_name = _('Person From Film')
        verbose_name_plural = _('Persons From Film')

        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='film_work_person_role'),
        ]
        indexes = [
            models.Index(fields=['film_work', 'person', 'role']),
        ]

    def __str__(self):
        """Verbose representation of PersonFilmwork entry.

        Returns:
             str
        """
        return f'{self.role} {self.person.full_name}'


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Stores a single filmwork entry, related to :model:`movies.Genre`."""

    title = models.TextField(_('title'))
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'), blank=True)
    rating = models.FloatField(_('rating'), blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(100),
    ])
    type = models.CharField(_('type'), choices=FilmworkType.choices, max_length=15)

    class Meta:
        """Meta information on :model:`movies.Filmwork`."""

        db_table = '"content"."film_work"'
        verbose_name = _('Film')
        verbose_name_plural = _('Films')

        constraints = [
            models.UniqueConstraint(fields=['title', 'creation_date'], name='film_work_creation_date'),
        ]
        indexes = [
            models.Index(fields=['title', 'creation_date']),
        ]

    def __str__(self):
        """Verbose representation of Filmwork entry."""
        return self.title
