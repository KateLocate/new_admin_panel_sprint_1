from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description', 'id')


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)

    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')
    list_filter = ('type', 'rating', 'genres')
    search_fields = ('title', 'description', 'id')
