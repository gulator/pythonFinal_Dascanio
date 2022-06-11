# Generated by Django 4.0.4 on 2022-06-05 01:42

import Blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=Blog.models.ruta),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=Blog.models.ruta),
        ),
        migrations.AlterField(
            model_name='posteo',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=Blog.models.ruta),
        ),
    ]