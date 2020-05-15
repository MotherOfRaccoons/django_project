from django.urls import path
from .views import (
    UserPostListView,
    UserDetailView
)

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user-profile'),
    path('<str:username>/posts', UserPostListView.as_view(), name='user-posts'),
]
