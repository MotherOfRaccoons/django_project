from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import UserRating, Rating


class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title_ru__icontains=query) |
                         Q(title_en__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    released = models.DateField()
    duration = models.PositiveSmallIntegerField()
    poster = models.ImageField(default="no_image.png", upload_to="movie_posters")
    ratings = GenericRelation(Rating, related_query_name='movies')

    objects = PostManager()

    def __str__(self):
        return self.title
