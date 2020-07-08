from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Article, Category
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import CategoryForm, FullSearchForm
from django.db.models import Q


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = "articles"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ArticleView(DetailView):
    template_name = 'article_detail.html'
    context_key = 'article'
    model = Article


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
    # paginate_by = 2
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
