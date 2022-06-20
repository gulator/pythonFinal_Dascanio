from time import strftime
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from Blog.models import *
from Blog.forms import *
from datetime import *
from . import views
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import random




# Create your views here.


def inicio (request):    
    avatares = Avatar.objects.filter(user=request.user.id)
    archivos = ['image1.jpg','image2.jpg','image3.jpg','image4.jpg','image5.jpg','image6.jpg','image7.jpg','image8.jpg','image9.jpg','image10.jpg']
    portada = random.choice(archivos)    

    if avatares:                                  
        return render (request,'inicio.html', {'avatar':avatares[0].imagen.url,'portada':portada})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'

    documento = {'avatar':no_avatar,'portada':portada}
    return render (request,'inicio.html',documento)


def paginas (request):
    paginas = Posteo.objects.all()       
    avatares = Avatar.objects.filter(user=request.user.id)
    
    if avatares:                                  
        return render (request,'paginas.html', {'avatar':avatares[0].imagen.url,'paginas':paginas})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'

    documento = {'paginas':paginas,'avatar':no_avatar}
    return render (request,'paginas.html',documento)


@login_required
def pagina_single(request, id):   

    pagina = Posteo.objects.get(id=id)
    avatares = Avatar.objects.filter(user=request.user.id)
    autor = request.user.username
    mensajes = Mensaje.objects.filter(id_clase=id)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   

    if request.method == 'POST':  #Crea los mensajes para cada pagina individual
        formulario = Mensaje_formulario(request.POST, request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data
            mensaje = Mensaje(autor = datos['autor'],fecha = datos['fecha'],avatar = datos['avatar'],comentario = datos['comentario'],id_clase=datos['id_clase'])
            mensaje.save()
        else:
            print ("formulario invalido!")    

    if avatares:                                  
        return render (request,'pagina.html', {'pagina':pagina,'avatar':avatares[0].imagen.url,'mensajes':mensajes,'autor':autor,'fecha':fecha})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'               
    
    return render (request,'pagina.html', {'pagina':pagina,'avatar':no_avatar,'mensajes':mensajes,'autor':autor,'fecha':fecha})


def peliculas (request):
    peliculas = Pelicula.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)

    if avatares:                                  
        return render (request,'peliculas.html', {'peliculas':peliculas,'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'    

    documento = {'peliculas':peliculas,'avatar':no_avatar}
    return render (request,'peliculas.html',documento)

@login_required
def pelicula_single(request, id):   

    pelicula = Pelicula.objects.get(id=id)
    avatares = Avatar.objects.filter(user=request.user.id)
    autor = request.user.username
    mensajes = Mensaje.objects.filter(id_clase=id)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     

    if request.method == 'POST':
        formulario = Mensaje_formulario(request.POST, request.FILES)
        print(formulario)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            mensaje = Mensaje(autor = datos['autor'],fecha = datos['fecha'],comentario = datos['comentario'],id_clase=datos['id_clase'],pelicula = datos['pelicula'],clase = datos['clase'],)
            mensaje.save()
        else:
            print ("formulario invalido!")    

    if avatares:                                  
        return render (request,'pelicula.html', {'pelicula':pelicula,'avatar':avatares[0].imagen.url,'mensajes':mensajes,'autor':autor,'fecha':fecha})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'               
    
    return render (request,'pelicula.html', {'pelicula':pelicula,'avatar':no_avatar,'mensajes':mensajes,'autor':autor,'fecha':fecha})

@login_required
def pelicula_borrar(request, id):
    pelicula = Pelicula.objects.get(id=id)
    pelicula.delete()
    peliculas = Pelicula.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)

    if avatares:                                  
        return render (request,'peliculas.html', {'peliculas':peliculas,'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'

    documento = {'peliculas':peliculas,'avatar':no_avatar}

    return render (request,'peliculas.html',documento)

@login_required
def editar_pelicula(request, id):
    pelicula = Pelicula.objects.get(id=id)
    avatares = Avatar.objects.filter(user=request.user.id)

    if request.method == 'POST':
        formulario = Editar_Pelicula_Formulario(request.POST)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            pelicula.nombre = datos['nombre']
            pelicula.trama_breve = datos['trama_breve']
            pelicula.trama_larga = datos['trama_larga']
            pelicula.anio = datos['anio']
            pelicula.save()

            pelicula = Pelicula.objects.get(id=id)

            return render(request, 'pelicula.html', {'pelicula':pelicula})

    else: 
                
        formulario = Pelicula_formulario(initial={'nombre':pelicula.nombre,'trama_breve':pelicula.trama_breve,'trama_larga':pelicula.trama_larga,'anio':pelicula.anio})        

    if avatares:                                  
        return render (request,'form_editar_pelicula.html', {'formulario':formulario,'pelicula':pelicula,'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'       

    return render (request,'form_editar_pelicula.html',{'formulario':formulario,'pelicula':pelicula,'avatar':no_avatar})

@login_required
def editar_imagen_pelicula(request, id):
    imagen = Pelicula.objects.get(id=id)
    avatares = Avatar.objects.filter(user=request.user.id)

    if request.method == 'POST':
        formulario = Editar_Imagen(request.POST, request.FILES)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            imagen.imagen=datos['imagen']
            imagen.save()
            
            if avatares:                                  
                return render (request,'pelicula.html', {'pelicula':imagen,'avatar':avatares[0].imagen.url})
            else:
                no_avatar = '/static/Blog/assets/img/noavatar.webp'
            documento = {'pelicula':imagen,'avatar':no_avatar}

            return render (request,'pelicula.html',documento)

    if avatares:                                  
        return render (request,'editar_imagen_pelicula.html', {'imagen':imagen,'avatar':avatares[0].imagen.url})
    else:
        no_avatar = '/static/Blog/assets/img/noavatar.webp'    

    return render(request,'editar_imagen_pelicula.html',{'imagen':imagen,'avatar':no_avatar})


@login_required
def alta_pelicula (request):
    avatares = Avatar.objects.filter(user=request.user.id)

    if request.method == 'POST':
        formulario = Pelicula_formulario(request.POST, request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data            
            pelicula = Pelicula(nombre = datos['nombre'],trama_breve = datos['trama_breve'],trama_larga = datos['trama_larga'],anio = datos['anio'],imagen = datos['imagen'])
            pelicula.save()            
            peliculas = Pelicula.objects.all()

            if avatares:                                  
                return render (request,'peliculas.html', {'peliculas':peliculas,'avatar':avatares[0].imagen.url})
            else:
                no_avatar =   '/static/Blog/assets/img/noavatar.webp'
            documento = {'peliculas':peliculas,'avatar':no_avatar}

            return render (request, 'peliculas.html',documento)
        else:
            texto = f"error en uno de los campos"
            return render (request,'alta_peliculas.html',{'texto':texto})
    
    return render (request,'alta_peliculas.html')

@login_required
def eliminar_mensaje (request,id):
    avatares = Avatar.objects.filter(user=request.user.id)
    mensaje = Mensaje.objects.get(id=id)
    mensaje.delete()

    peliculas = Pelicula.objects.all()
    paginas = Posteo.objects.all()
    mensajes = Mensaje.objects.all()

    if avatares:                                  
        return render (request,'panel.html', {'avatar':avatares[0].imagen.url,'peliculas':peliculas,'paginas':paginas,'mensajes':mensajes})
    else:
        no_avatar = '/static/Blog/assets/img/noavatar.webp'
        return render (request, 'panel.html', {'avatar':no_avatar,'peliculas':peliculas,'paginas':paginas,'mensajes':mensajes})

@login_required
def editar_mensaje (request,id):
    avatares = Avatar.objects.filter(user=request.user.id)
    comentario = Mensaje.objects.get(id=id)

    if request.method == 'POST':
        formulario = Editar_Mensaje_formulario(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            print (datos)
            comentario.fecha = datos['fecha']
            comentario.editado = datos['editado']
            comentario.comentario = datos['comentario']
            comentario.save()

            peliculas = Pelicula.objects.all()
            paginas = Posteo.objects.all()
            mensajes = Mensaje.objects.all()

            if avatares:                                  
                return render (request,'panel.html', {'avatar':avatares[0].imagen.url,'peliculas':peliculas,'paginas':paginas,'mensajes':mensajes})
            else:
                no_avatar = '/static/Blog/assets/img/noavatar.webp'
                return render (request, 'panel.html', {'avatar':no_avatar,'peliculas':peliculas,'paginas':paginas,'mensajes':mensajes})           
            
        else:
            texto = f'error en uno de los campos'
            return render(request,'inicio.html',{'texto':texto})

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    if avatares:                       
        return render (request,'form_editar_mensaje.html',{'fecha':fecha,'avatar':avatares[0].imagen.url,'comentario':comentario})
    else:
        no_avatar = '/static/Blog/assets/img/noavatar.webp'

    return render (request,'form_editar_mensaje.html',{'fecha':fecha,'avatar':no_avatar,'comentario':comentario})

def buscar_mensajes (request):
    avatares = Avatar.objects.filter(user=request.user.id)
    pelicula = Pelicula.objects.all()
    pagina = Posteo.objects.all()
    texto = f'Ingrese un texto en el campo de búsqueda"'

    if request.GET['autor']:
        autor = request.GET['autor']
        mensajes = Mensaje.objects.filter(autor__icontains=autor)
        texto2 = f'no se han encontrado comentarios hechos por "{autor}"'

        if mensajes:
            
            if avatares:                       
                return render (request,'res_busc_mensaje.html',{'mensajes':mensajes,'avatar':avatares[0].imagen.url,'pagina':pagina,'pelicula':pelicula,'autor':autor})
            else:
                no_avatar = '/static/Blog/assets/img/noavatar.webp'
                return render (request,'res_busc_mensaje.html',{'mensajes':mensajes,'avatar':no_avatar,'pagina':pagina,'pelicula':pelicula,})
        else:
            
            if avatares:                       
                return render (request,'res_busc_mensaje.html',{'mensajes':mensajes,'avatar':avatares[0].imagen.url,'pagina':pagina,'pelicula':pelicula,'autor':autor,'texto2':texto2})
            else:
                no_avatar = '/static/Blog/assets/img/noavatar.webp'
                return render (request,'res_busc_mensaje.html',{'mensajes':mensajes,'avatar':no_avatar,'pagina':pagina,'pelicula':pelicula,'texto2':texto2})

    else:
        if avatares:                       
            return render (request,'res_busc_mensaje.html',{'avatar':avatares[0].imagen.url,'pagina':pagina,'pelicula':pelicula,'texto':texto})
        else:
            no_avatar = '/static/Blog/assets/img/noavatar.webp'
            return render (request,'res_busc_mensaje.html',{'avatar':no_avatar,'pagina':pagina,'pelicula':pelicula,'texto':texto})



@login_required
def alta_pagina (request):    

    if request.method == 'POST':
        formulario = Pagina_formulario(request.POST,request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data
            pagina = Posteo(titulo = datos['titulo'],subtitulo = datos['subtitulo'],pelicula = datos['pelicula'],cuerpo = datos['cuerpo'],autor = datos['autor'],fecha = datos['fecha'],imagen = datos['imagen'],)
            pagina.save()
            texto = f'Post creado con exito'
            return render(request,'paginas.html',{'texto':texto})
        else:
            texto = f'error en uno de los campos'
            return render(request,'alta_paginas.html',{'texto':texto})

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usuario = request.user.username 
            
    return render (request,'alta_paginas.html',{'fecha':fecha,'usuario':usuario})



def buscar_pelicula(request):    
    
        if request.GET['nombre']:
            nombre = request.GET['nombre']
            peliculas = Pelicula.objects.filter(nombre__icontains=nombre)
            if peliculas:
                return render (request,'res_busc_peli.html', {'peliculas':peliculas,'peli':nombre})
            else:
                peliculas = Pelicula.objects.all()
                texto2 = f'no se han encontrado peliculas conteniendo "{nombre}"'
                return render (request,'peliculas.html', {"peliculas":peliculas,"texto2":texto2})   
        else:
            peliculas = Pelicula.objects.all()
            texto = f'Ingrese un texto en el campo de búsqueda'
            return render (request,'peliculas.html', {"peliculas":peliculas,"texto":texto})

    #return render(request,'buscar_peliculas.html')    

def buscar_pagina (request):
    if request.GET['pelicula']:
            nombre = request.GET['pelicula']
            paginas = Posteo.objects.filter(pelicula__icontains=nombre)

            if paginas:
                return render (request,'res_busc_pagina.html', {'paginas':paginas,'nombre':nombre})
            else:
                paginas = Posteo.objects.all()
                texto2 = f'no se han encontrado peliculas conteniendo "{nombre}"'
                return render (request,'paginas.html', {"paginas":paginas,"texto2":texto2})   

    else:
        paginas = Posteo.objects.all()
        texto = f'Ingrese un texto en el campo de búsqueda'
        return render (request,'paginas.html', {"paginas":paginas,"texto":texto})

@login_required
def eliminar_pagina(request, id):
        pagina = Posteo.objects.get(id=id)
        pagina.delete()
        paginas = Posteo.objects.all()
        return render (request,'paginas.html',{"paginas":paginas})


@login_required
def editar_pagina (request, id):
    paginas = Posteo.objects.get(id=id)     
    
    if request.method == 'POST':
        formulario = Editar_Pagina_formulario(request.POST)            
        print(formulario)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            paginas.titulo = datos['titulo']
            paginas.subtitulo = datos['subtitulo']
            paginas.pelicula = datos['pelicula']
            paginas.cuerpo = datos['cuerpo']
            paginas.autor = datos['autor']
            paginas.fecha = datos['fecha']
            paginas.editado = datos['editado']            
            paginas.save()

            paginas = Posteo.objects.all()           
            return render (request,'paginas.html',{"paginas":paginas})
        else:
            texto = f"algunos campos contienen errores"
            #return HttpResponse(texto)
            return render (request, 'form_editar_pagina.html', {'paginas':paginas, 'texto':texto})
    

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    usuario = request.user.username
    return render (request,'form_editar_pagina.html', {'paginas':paginas,'fecha':fecha, 'usuario':usuario})

@login_required
def editar_imagen_pagina (request, id):
    imagen = Posteo.objects.get(id=id)

    if request.method == 'POST':
        formulario = Editar_Imagen(request.POST,request.FILES)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            imagen.imagen = datos['imagen']
            imagen.save()

            #paginas = Posteo.objects.all()
            pagina = Posteo.objects.get(id=id)
            return render(request,'pagina.html',{'pagina':pagina})
        else:
            texto = f'la imagen no es de un formato valido'
            pagina = Posteo.objects.get(id=id)
            return render(request,'pagina.html',{'pagina':pagina,'texto':texto})

    else: 
                
        formulario = Pagina_formulario(initial={'imagen':imagen.imagen})

    return render (request,'editar_imagen_pagina.html', {'formulario':formulario,'imagen':imagen})

@login_required
def perfil (request, id):

    datos = request.user
    avatares = Avatar.objects.filter(user=request.user.id)
    usuario = request.user.username
    posteos = Posteo.objects.filter(autor=request.user.username)
    mensajes = Mensaje.objects.filter(autor=request.user.username)

    if avatares:                                  
        return render (request,'perfil.html', {'avatar':avatares[0].imagen.url,'posteos':posteos,'datos':datos,'mensajes':mensajes})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'
    documento = {'avatar':no_avatar, 'usuario':usuario,'posteos':posteos,'datos':datos,'mensajes':mensajes}

    return render (request, 'perfil.html',documento)

@login_required
def panel (request):
    peliculas = Pelicula.objects.all()
    paginas = Posteo.objects.all()
    mensajes = Mensaje.objects.all()

    datos = {'peliculas':peliculas,'paginas':paginas,'mensajes':mensajes}


    return render (request,'panel.html',datos)

def acerca(request):
    return render (request, 'acerca.html')


