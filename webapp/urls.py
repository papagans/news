from django.contrib import admin
from django.urls import path
from .views import IndexView, ArticleView, CategoryView, CategoryUpdateView, CategoryDeleteView, CategoryCreateView, \
    ArticleUpdateView, ArticleCreateView, ArticleDeleteView, ArticleListView, SearchResultsView

app_name ='webapp'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_detail'),
    path('article/edit/<int:pk>/', ArticleUpdateView.as_view(), name='article_edit'),
    path('article/add/', ArticleCreateView.as_view(), name='article_add'),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='category_edit'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/add/', CategoryCreateView.as_view(), name='category_add'),
    path('article_category/<int:pk>', ArticleListView.as_view(), name='article_category'),
    path('article/search/results/', SearchResultsView.as_view(), name='search_results'),
]