# Generated by Django 4.0.4 on 2022-05-26 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(help_text=' Выберите автора книги', to='catalog.author', verbose_name='Автор книги'),
        ),
    ]
