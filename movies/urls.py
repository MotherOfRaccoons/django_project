from django.urls import path
from .views import (
    MovieListView
)
from . import views
from .views import SearchView, MovieDetailView, AddToCompletedView, AddToPlannedView, RemoveFromList, handle_rating

urlpatterns = [
    path('', MovieListView.as_view(), name='movie-home'),
    path('search/', SearchView.as_view(), name='search-movie'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('completed/add/', AddToCompletedView.as_view(), name='add-to-completed'),
    path('planned/add/', AddToPlannedView.as_view(), name='add-to-planned'),
    path('remove', RemoveFromList.as_view(), name='remove-from-lists'),
    path('change_rating', handle_rating, name='change-rating'),
]
