from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Movie


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
