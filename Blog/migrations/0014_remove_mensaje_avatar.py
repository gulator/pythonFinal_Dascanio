# Generated by Django 4.0.4 on 2022-06-20 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0013_alter_mensaje_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensaje',
            name='avatar',
        ),
    ]
