from django import forms
from .models import Category
from django.core.exceptions import ValidationError


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'subcategory']

    def clean_category_name(self):
        title = self.cleaned_data.get('title')
        if Category.objects.filter(title__icontains=title):
            raise ValidationError('Категория с таким названием уже существует!')
        else:
            return title


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=20, required=False, label='Поиск')


class EasterEggForm(forms.Form):
    text = forms.CharField(max_length=2, required=False, label='Введите последние две цыфры моего телефона')

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text != '39':
            raise ValidationError('А вот и нет!')
        else:
            return text
