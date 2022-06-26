"""Admin panel configuration for movies app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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
    autocomplete_fields = ('person',)


class GenreFilmworkInline(admin.TabularInline):
    """Represents admin options for GenreFilmwork model as inline block."""

    model = GenreFilmwork
    autocomplete_fields = ('genre',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Represents admin options and functionality for Filmwork model."""

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _('Film Genres')

    list_display = (
        'title',
        'get_genres',
        'creation_date',
        'rating',
        'modified',
    )

    list_prefetch_related = ('genres', 'persons')
    list_filter = ('type', 'rating', 'genres')
    search_fields = ('title', 'description', 'id')

    inlines = (GenreFilmworkInline, PersonFilmworkInline)
