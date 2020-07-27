# Generated by Django 2.2 on 2020-07-08 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20200708_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category_id', to='webapp.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='webapp.Category', verbose_name='Подкатегории'),
        ),
    ]