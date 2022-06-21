"""
Apps Configuration
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoviesConfig(AppConfig):
    """Class representing the app 'movies' with its configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = _('movies')
