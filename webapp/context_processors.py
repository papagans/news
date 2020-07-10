from .models import Category
from .forms import FullSearchForm, EasterEggForm


def category(request):
    return {"categories": Category.objects.all()}


def get_search_form(request):
    search_form = FullSearchForm(request.GET or None)
    return {"search_form": search_form}


def favorite_counter(request):
    counter = request.session.get('favorites')
    if counter:
        counter = len(request.session.get('favorites'))
    else:
        counter = 0
    return {"favorite_counter": counter}


def easter_egg_form(request):
    easter_egg_form = EasterEggForm(request.GET or None)
    return {"easter_egg_form": easter_egg_form}
