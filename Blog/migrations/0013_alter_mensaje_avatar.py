# Generated by Django 4.0.4 on 2022-06-19 05:27

import Blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0012_remove_mensaje_id_avatar_mensaje_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=Blog.models.ruta),
        ),
    ]
