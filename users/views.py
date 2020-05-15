from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic import (
    DetailView, ListView
)
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import User, MovieList
from blog.models import Post


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f' Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
        else:
            request.user = User.objects.filter(id=request.user.id).first()
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


#   Selected user's posts
class UserPostListView(ListView):
    model = Post
    template_name = 'users/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = MovieList.objects.filter(user_id=self.kwargs.get('pk'))
        completed = user_list.filter(status__status='Completed')
        context['completed'] = completed
        context['planned'] = user_list.filter(status__status='Planned')
        context['favorite'] = user_list.filter(status__status='Favorite')
        watchtime_mins = completed.aggregate(Sum('movie__duration'))['movie__duration__sum'] or 0
        context['watchtime'] = format(watchtime_mins / 60, '.2f')
        context['logged_in_user'] = self.request.user
        return context
