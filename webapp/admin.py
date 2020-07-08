from django.contrib import admin

# Register your models here.
from .models import Category, Article


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'subcategory']
    list_filter = ['title']
    list_display_links = ['pk', 'title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category_id', 'user_id', 'title', 'description', 'image']
    list_filter = ['title']
    list_display_links = ['pk', 'title', 'user_id', 'category_id']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)