# Generated by Django 2.2 on 2020-07-10 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20200708_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_id', to='webapp.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.Category', verbose_name='Родительская категория'),
        ),
    ]