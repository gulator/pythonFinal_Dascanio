from distutils.command.upload import upload
from pyexpat import model
from django.db import models
import datetime
import os
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


def ruta (request, filename):
    nombre_viejo = filename
    hora = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    nombre_nuevo = "%s%s" % ( hora, nombre_viejo)
    return os.path.join ('', nombre_nuevo)

class Posteo (models.Model):  #La clase pertenece a todo lo referido a "paginas"
    titulo = models.CharField(max_length=80)
    subtitulo = models.CharField(max_length=80)
    pelicula = models.CharField(max_length=60)
    cuerpo = RichTextField(blank=True, null=True)
    #cuerpo = models.TextField()
    autor = models.CharField(max_length=40)
    fecha = models.DateTimeField()
    editado = models.CharField(max_length=10)
    imagen = models.ImageField(upload_to = ruta, null=True, blank=True)

    def __str__(self):
        return f'Titulo: {self.titulo} | Subtitulo: {self.subtitulo}'

class Pelicula (models.Model):
    nombre = models.CharField(max_length=60)
    trama_breve = models.CharField(max_length=250)
    trama_larga = models.TextField()
    anio = models.IntegerField()
    imagen = models.ImageField(upload_to = ruta, null=True, blank=True)

    def __str__(self):
        return f'Pelicula: {self.nombre}'

class Mensaje (models.Model):
    autor = models.CharField(max_length=60)
    fecha = models.DateTimeField()
    editado = models.CharField(max_length=10)       
    comentario = models.TextField()
    id_clase = models.IntegerField()
    clase = models.CharField(max_length=10)
    pelicula = models.CharField(max_length=60)

    def __str__(self):
        return f'Comentario de {self.autor} en {self.clase} referida a pelicula: {self.pelicula}'

class Avatar (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

    def __str__(self):
        return f'Avatar usuario: {self.user}'


