from django import forms
from .models import Category
from django.core.exceptions import ValidationError


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'subcategory']

    def clean_category_name(self):
        title = self.cleaned_data.get('title')
        # if Category.objects.filter(title__iexact=title):
        if Category.objects.filter(title__icontains=title):
            raise ValidationError('Категория с таким названием уже существует!')
        else:
            return title