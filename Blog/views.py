from time import strftime
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from Blog.models import *
from Blog.forms import *
from datetime import *

from . import views

# Create your views here.

def inicio (request):
    return render (request,'inicio.html')


def paginas (request):
    paginas = Posteo.objects.all()
    documento = {'paginas':paginas}
    return render (request,'paginas.html',documento)


def posteos (request):
    return render (request,'posteos.html')


def peliculas (request):
    peliculas = Pelicula.objects.all()
    documento = {'peliculas':peliculas}
    return render (request,'peliculas.html',documento)


def mensajes (request):
    mensajes = Mensaje.objects.all()
    documento = {'mensajes':mensajes}
    return render (request,'mensajes.html',documento)


def alta_pelicula (request):
    if request.method == 'POST':
        formulario = Pelicula_formulario(request.POST, request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data            
            pelicula = Pelicula(nombre = datos['nombre'],trama_breve = datos['trama_breve'],trama_larga = datos['trama_larga'],anio = datos['anio'],imagen = datos['imagen'])
            pelicula.save()
            texto = f"Pelicula cargada con éxito"
            return render (request, 'alta_peliculas.html',{'texto':texto})
        else:
            texto = f"error en uno de los campos"
            return render (request,'alta_peliculas.html',{'texto':texto})
    
    return render (request,'alta_peliculas.html')


def alta_mensaje (request):
    if request.method == 'POST':
        formulario = Mensaje_formulario(request.POST,request.FILES)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            mensaje = Mensaje(autor = datos['autor'],fecha = datos['fecha'],avatar = datos['avatar'],comentario = datos['comentario'])
            mensaje.save()
            texto = f'mensaje cargado con exito'
            return render(request,'alta_mensajes.html',{'texto':texto})
        else:
            texto = f'error en uno de los campos'
            return render(request,'alta_mensajes.html',{'texto':texto})

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
    return render (request,'alta_mensajes.html',{'fecha':fecha})

def alta_pagina (request):
    if request.method == 'POST':
        formulario = Pagina_formulario(request.POST,request.FILES)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            pagina = Posteo(titulo = datos['titulo'],subtitulo = datos['subtitulo'],pelicula = datos['pelicula'],cuerpo = datos['cuerpo'],autor = datos['autor'],fecha = datos['fecha'],imagen = datos['imagen'],)
            pagina.save()
            texto = f'pagina cargada con exito'
            return render(request,'alta_mensajes.html',{'texto':texto})
        else:
            texto = f'error en uno de los campos'
            return render(request,'alta_paginas.html',{'texto':texto})

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
    return render (request,'alta_paginas.html',{'fecha':fecha})    
