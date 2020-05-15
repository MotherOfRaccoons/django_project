from django.urls import path
from .views import (
    MovieListView
)
from . import views
from .views import SearchView

urlpatterns = [
    path('', MovieListView.as_view(), name='movie-home'),
    path('search/', SearchView.as_view(), name='search-movie'),
]
