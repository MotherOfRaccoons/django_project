from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import Movie


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

