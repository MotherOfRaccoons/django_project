from django.shortcuts import HttpResponseRedirect, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Movie, UserRating
from users.models import Profile, MovieList, FollowingRelation, Event


def get_list_context(user):
    context = {'user': user}

    if not user.is_anonymous:
        completed_movies = [
            entry.movie for entry in MovieList.objects.filter(user=user, status__status='Completed')
        ]
        planned_movies = [
            entry.movie for entry in MovieList.objects.filter(user=user, status__status='Planned')
        ]
        context['completed_movies'] = completed_movies
        context['planned_movies'] = planned_movies

    return context


class SearchView(ListView):
    template_name = 'movies/home.html'
    context_object_name = 'movies'
    paginate_by = 5
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        context.update(get_list_context(self.request.user))

        user_qs = Profile.objects.search(query=self.request.GET.get('q', None))[:5]
        context['user_count'] = len(user_qs) or 0
        context['found_users'] = user_qs

        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            qs = Movie.objects.search(query=query)
            self.count = len(qs)
            return qs
        return Movie.objects.none()


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/home.html'
    context_object_name = 'movies'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_list_context(self.request.user))
        return context


class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_list_context(self.request.user))
        return context


class AddToCompletedView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        next_page = request.GET.get("next")
        movie = Movie.objects.get(id=request.GET.get("movie_id"))
        entry = MovieList.objects.filter(user=user, movie=movie)
        if entry.exists():
            entry.delete()
        list_entry = MovieList.objects.create_completed_entry(user=user, movie=movie)
        list_entry.save()
        # create event
        event = Event(user=user, movie=movie, event='Added to completed')
        event.save()
        return HttpResponseRedirect(next_page)


class AddToPlannedView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        next_page = request.GET.get("next")
        movie = Movie.objects.get(id=request.GET.get("movie_id"))
        entry = MovieList.objects.filter(user=user, movie=movie)
        if entry.exists():
            entry.delete()
        list_entry = MovieList.objects.create_planned_entry(user=user, movie=movie)
        list_entry.save()
        # remove rating
        rating = UserRating.objects.filter(user=user, rating_id__object_id=movie.id)
        if rating.exists():
            rating.delete()
        # create event
        event = Event(user=user, movie=movie, event='Added to planned')
        event.save()
        return redirect(next_page)


class RemoveFromList(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get("next")
        movie = Movie.objects.get(id=request.GET.get("movie_id"))
        entry = MovieList.objects.filter(user=self.request.user, movie=movie)
        entry.delete()
        # remove rating
        rating = UserRating.objects.filter(user=self.request.user, rating_id__object_id=movie.id)
        if rating.exists():
            rating.delete()
        return HttpResponseRedirect(next_page)


def handle_rating(request):
    user = request.user
    movie = Movie.objects.filter(id=request.GET.get('id', None)).get()
    entry = MovieList.objects.filter(user=user, movie=movie)

    if not entry.exists() or (entry.get().status.status != 'Completed'):
        entry.delete()
        list_entry = MovieList.objects.create_completed_entry(user=user, movie=movie)
        list_entry.save()
        changed = True
        event = Event(user=user, movie=movie, event='Added to completed')
        event.save()
    else:
        changed = False

    rating = request.GET.get('rating', None)
    event = Event(user=user, movie=movie, event=f'Rated {rating} <i class="fas fa-star"></i>')
    event.save()

    return JsonResponse({'changed': changed})


class EventListView(ListView):
    model = Event
    template_name = 'users/events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        following_relation = FollowingRelation.objects.all().filter(following=self.request.user).values()
        followed = [x['followed_id'] for x in following_relation]
        events = Event.objects.all().filter(user_id__in=followed).order_by('-time')
        return events
