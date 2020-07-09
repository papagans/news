from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Article, Category
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CategoryForm, FullSearchForm
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = "articles"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        views = self.request.GET.get('views')
        date = self.request.GET.get('date')
        if date:
            context['articles'] = Article.objects.order_by('-date')
        if views:
            context['articles'] = Article.objects.order_by('-views')
        return context


class ArticleView(DetailView):
    template_name = 'article_detail.html'
    context_key = 'article'
    model = Article

    def get_context_data(self, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs['pk'])
        article.views += 1  # инкрементируем счётчик просмотров и обновляем поле в базе данных
        article.save(update_fields=['views'])
        context = super().get_context_data(**kwargs)
        context['views'] = article.views
        return context


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'partial/edit.html'
    context_key = 'article'
    model = Article
    fields = ['title', 'description', 'image', 'user_id', 'category_id']
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class ArticleCreateView(UserPassesTestMixin, CreateView):
    model = Article
    template_name = 'partial/add.html'
    fields = ['title', 'description', 'image', 'user_id', 'category_id']
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    context_object_name = 'object'
    template_name = 'partial/delete.html'
    success_url = reverse_lazy('webapp:index')
    permission_required = "webapp.delete_article"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff


class CategoryView(ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = "categories"


class CategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Category
    template_name = 'partial/edit.html'
    fields = ['title', 'subcategory']
    context_object_name = 'category'
    success_url = reverse_lazy('webapp:categories')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class CategoryDeleteView(UserPassesTestMixin, DeleteView):
    model = Category
    context_object_name = 'object'
    template_name = 'partial/delete.html'
    success_url = reverse_lazy('webapp:categories')
    permission_required = "webapp.delete_category"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff


class CategoryCreateView(UserPassesTestMixin, CreateView):
    model = Category
    template_name = 'partial/add.html'
    form_class = CategoryForm
    success_url = reverse_lazy('webapp:categories')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class ArticleListView(ListView):
    template_name = 'index.html'
    model = Article

    def get_url(self):
        global site
        site = self.request.path
        return site

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['articles'] = Article.objects.filter(category_id=self.kwargs.get('pk'))
        self.get_url()
        return context


class SearchResultsView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'articles'
    # paginate_by = 3
    # paginate_orphans = 1

    def get_url(self):
        global site
        site = self.request.get_full_path()
        return site

    def get_context_data(self, *, text=None, **kwargs):
        form = FullSearchForm(data=self.request.GET)
        if form.is_valid():
            text = form.cleaned_data.get("text")
            query = self.get_query_string()
            articles = Article.objects.filter(Q(title__icontains=text))
            return super().get_context_data(form=form, query=query, articles=articles)

    def get_query_string(self):
        data = {}
        for key in self.request.GET:
            if key != 'page':
                data[key] = self.request.GET.get(key)
        return data


class FavoriteView(ListView):
    model = Article
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites = self._prepare_favorites()
        context['articles'] = favorites
        context['favorites'] = Article.objects.all()
        return context

    def _prepare_favorites(self):
        favorites = self.request.session.get('favorites', [])
        favorite_list = []
        for pk in favorites:
            article = Article.objects.get(pk=pk)
            favorite_list.append(article)
        return favorite_list


def favoriteadditem(request):
    articles = request.session.get('favorites', [])
    pk = request.POST.get('pk')
    article = get_object_or_404(Article, pk=request.POST.get('pk'))
    articles.append(pk)
    request.session['favorites'] = articles  # Храню в сессии избранные новости
    return JsonResponse({'pk': article.pk})


def favoritedeleteitem(request):
    articles = request.session.get('favorites', [])
    pk = request.POST.get('pk')
    for article_pk in articles:
        if article_pk == pk:
            articles.remove(article_pk)
            break
    request.session['favorites'] = articles
    return JsonResponse({'pk': articles})