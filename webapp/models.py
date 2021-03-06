from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Категория')
    subcategory = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True,
                                    blank=True, verbose_name="Родительская категория")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    category_id = models.ForeignKey(Category, related_name='category_id', on_delete=models.SET_NULL, null=True,
                                    blank=True, verbose_name='Категория')
    user_id = models.ForeignKey(User, related_name='user_id', on_delete=models.PROTECT, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=3000, verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(upload_to='article_image', null=True, blank=True, verbose_name='Фото')
    date = models.DateTimeField(auto_now_add=True,
                                verbose_name='Дата добавления')  # добавил дату создания новости, для вывода новвых новостей
    views = models.IntegerField('Просмотры', default=0)  # добавил счетчик просмотров Новостей

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
