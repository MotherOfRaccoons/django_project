from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Movie
from users.models import User, MovieList


class SearchView(ListView):
    template_name = 'movies/home.html'
    context_object_name = 'movies'
    paginate_by = 5
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
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
        context['user'] = self.request.user
        completed_movies = [
            entry.movie for entry in MovieList.objects.filter(user=self.request.user, status__status='Completed')
        ]
        planned_movies = [
            entry.movie for entry in MovieList.objects.filter(user=self.request.user, status__status='Planned')
        ]
        context['completed_movies'] = completed_movies
        context['planned_movies'] = planned_movies
        return context


class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        completed_movies = [
            entry.movie for entry in MovieList.objects.filter(user=self.request.user, status__status='Completed')
        ]
        planned_movies = [
            entry.movie for entry in MovieList.objects.filter(user=self.request.user, status__status='Planned')
        ]
        context['completed_movies'] = completed_movies
        context['planned_movies'] = planned_movies
        return context


class AddToCompletedView(View):

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get("next")
        movie = Movie.objects.get(id=request.GET.get("movie_id"))
        entry = MovieList.objects.filter(user=self.request.user, movie=movie)
        if entry.exists():
            entry.delete()
        list_entry = MovieList.objects.create_completed_entry(user=self.request.user, movie=movie)
        list_entry.save()
        return HttpResponseRedirect(next_page)


class AddToPlannedView(View):

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get("next")
        movie = Movie.objects.get(id=request.GET.get("movie_id"))
        entry = MovieList.objects.filter(user=self.request.user, movie=movie)
        if entry.exists():
            entry.delete()
        list_entry = MovieList.objects.create_planned_entry(user=self.request.user, movie=movie)
        list_entry.save()
        return redirect(next_page)


class RemoveFromList(View):

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get("next")
        movie = Movie.objects.get(id=request.GET.get("movie_id"))
        entry = MovieList.objects.filter(user=self.request.user, movie=movie)
        entry.delete()
        return HttpResponseRedirect(next_page)
