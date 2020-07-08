from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Article, Category
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import CategoryForm


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = "articles"


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
    # form_class = CategoryForm
    fields = ['title', 'description', 'image', 'user_id', 'category_id']
    success_url = reverse_lazy('webapp:index')

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
    #
    # def get_success_url(self):
    #     return reverse('webapp:categories')


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
