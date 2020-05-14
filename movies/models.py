from django.db import models
from django.db.models import Q


class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(description__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    released = models.DateField()
    duration = models.PositiveSmallIntegerField()
    poster = models.ImageField(default="no_image.png", upload_to="movie_posters")

    objects = PostManager()

    def __str__(self):
        return self.title
