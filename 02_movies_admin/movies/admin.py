"""Admin panel configuration for movies app."""

from django.contrib import admin

from movies.models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Represents admin options and functionality for Genre model."""

    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Represents admin options and functionality for Person model."""

    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name', 'id')


class PersonFilmworkInline(admin.TabularInline):
    """Represents admin options for PersonFilmwork model as inline block."""

    model = PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    """Represents admin options for GenreFilmwork model as inline block."""

    model = GenreFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Represents admin options and functionality for Filmwork model."""

    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'created',
        'modified',
    )
    list_filter = ('type', 'rating', 'genres')
    search_fields = ('title', 'description', 'id')
