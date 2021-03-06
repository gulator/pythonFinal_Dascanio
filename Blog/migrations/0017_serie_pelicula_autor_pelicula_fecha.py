# Generated by Django 4.0.4 on 2022-06-23 15:26

import Blog.models
import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0016_alter_pelicula_trama_larga'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('resumen', models.CharField(max_length=250)),
                ('trama', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('anio', models.IntegerField()),
                ('autor', models.CharField(max_length=40)),
                ('fecha', models.DateTimeField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=Blog.models.ruta)),
            ],
        ),
        migrations.AddField(
            model_name='pelicula',
            name='autor',
            field=models.CharField(default='null', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pelicula',
            name='fecha',
            field=models.DateTimeField(default='2022-06-20'),
            preserve_default=False,
        ),
    ]
