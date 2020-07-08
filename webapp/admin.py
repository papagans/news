from django.contrib import admin

# Register your models here.
from source.webapp.models import Category, Article


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'parent_id']
    list_filter = ['title']
    list_display_links = ['pk', 'title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category_id', 'user_id', 'title', 'description', 'image']
    list_filter = ['title']
    list_display_links = ['pk', 'title', 'user_id']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, CategoryAdmin)