from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    year = models.DateField()
    duration = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title
