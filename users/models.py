from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from movies.models import Movie
from PIL import Image


class ProfileManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(user__username__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwarg s):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class MovieStatus(models.Model):
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.status


class MovieListManager(models.Manager):
    def create_completed_entry(self, user, movie):
        list_entry = self.create(user=user, movie=movie, status=MovieStatus.objects.get(status='Completed'))
        return list_entry

    def create_planned_entry(self, user, movie):
        list_entry = self.create(user=user, movie=movie, status=MovieStatus.objects.get(status='Planned'))
        return list_entry


class MovieList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.ForeignKey(MovieStatus, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(default=timezone.now)

    objects = MovieListManager()

    def __str__(self):
        return f"{self.user}'s {self.status}"
