from .models import Category
from .forms import FullSearchForm


def category(request):
    return {"categories": Category.objects.all()}


def get_search_form(request):
    search_form = FullSearchForm(request.GET or None)
    return {"search_form": search_form}
