from .models import Movie


def get_top5_movies(requests):
    movies = Movie.objects.filter(ratings__isnull=False).order_by('ratings__average').reverse()[:5]
    return {"top5_movies": movies}
