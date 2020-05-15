from django.urls import path
from .views import (
    UserPostListView,
    UserDetailView
)

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user-posts'),
]
