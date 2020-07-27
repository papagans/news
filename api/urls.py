from django.urls import path
from .views import ArticleView, CategoryView
app_name = "api"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('categories/', CategoryView.as_view()),
]