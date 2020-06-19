from django.urls import path
from .views import (
    UserPostListView,
    UserDetailView,
    follow_user,
    unfollow_user
)

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user-profile'),
    path('<str:username>/posts', UserPostListView.as_view(), name='user-posts'),
    path('<int:user>/follow', follow_user, name='user-follow'),
    path('<int:user>/unfollow', unfollow_user, name='user-unfollow'),
]
