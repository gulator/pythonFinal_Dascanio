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




# Create your views here.

@login_required
def inicio (request):    
    avatares = Avatar.objects.filter(user=request.user.id)
    if avatares:                                  
        return render (request,'inicio.html', {'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'
    documento = {'avatar':no_avatar}
    return render (request,'inicio.html',documento)


def paginas (request):
    paginas = Posteo.objects.all()    
    avatares = Avatar.objects.filter(user=request.user.id)
    if avatares:                                  
        return render (request,'paginas.html', {'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'
    documento = {'paginas':paginas,'avatar':no_avatar}
    return render (request,'paginas.html',documento)


def posteos (request):
    return render (request,'posteos.html')


def peliculas (request):
    peliculas = Pelicula.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    if avatares:                                  
        return render (request,'peliculas.html', {'peliculas':peliculas,'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'    
    documento = {'peliculas':peliculas,'avatar':no_avatar}
    return render (request,'peliculas.html',documento)


def pelicula_single(request, id):    
    pelicula = Pelicula.objects.get(id=id)
    avatares = Avatar.objects.filter(user=request.user.id)
    if avatares:                                  
        return render (request,'pelicula.html', {'pelicula':pelicula,'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'
    documento = {'pelicula':pelicula,'avatar':no_avatar}        
    
    return render (request,'pelicula.html', documento)

@login_required
def pelicula_borrar(request, id):
    pelicula = Pelicula.objects.get(id=id)
    pelicula.delete()
    peliculas = Pelicula.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    if avatares:                                  
        return render (request,'pelicula.html', {'peliculas':peliculas,'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'
    documento = {'peliculas':peliculas,'avatar':no_avatar}

    return render (request,'peliculas.html',documento)

@login_required
def editar_pelicula(request, id):
    pelicula = Pelicula.request.get(id=id)

    if request.method == 'POST':
        formulario = Editar_Pelicula_Formulario(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            pelicula.nombre = datos['nombre']
            pelicula.trama_breve = datos['trama_breve']
            pelicula.trama_larga = datos['trama_larga']
            pelicula.anio = datos['anio']
            pelicula.save()

    return render (request,'form_editar_pelicula')

@login_required
def pelicula_editar_imagen(request, id):
    pass

@login_required
def mensajes (request):
    mensajes = Mensaje.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    if avatares:                                  
        return render (request,'mensajes.html', {'avatar':avatares[0].imagen.url})
    else:
        no_avatar =   '/static/Blog/assets/img/noavatar.webp'
    documento = {'mensajes':mensajes,'avatar':no_avatar}
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


@login_required
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

def buscar_pelicula (request):
    return render(request,'buscar_peliculas.html')   

def busca_pelicula(request):
    
        if request.GET['nombre']:
            nombre = request.GET['nombre']
            peliculas = Pelicula.objects.filter(nombre__icontains=nombre)
            return render (request,'res_busc_peli.html', {'peliculas':peliculas})
        else:
            texto = f'Ninguna pelicula encontrada en la base con ese nombre'
            return render (request,'res_busc_peli.html', {"texto":texto})

    #return render(request,'buscar_peliculas.html')    

def eliminar_post(request, id):
        pagina = Posteo.objects.get(id=id)
        pagina.delete()
        paginas = Posteo.objects.all()
        return render (request,'paginas.html',{"paginas":paginas})


@login_required
def editar_post (request, id):
    paginas = Posteo.objects.get(id=id)     
    
    if request.method == 'POST':
        formulario = Editar_Pagina_formulario(request.POST)            
        
        if formulario.is_valid():
            datos = formulario.cleaned_data
            paginas.titulo = datos['titulo']
            paginas.subtitulo = datos['subtitulo']
            paginas.pelicula = datos['pelicula']
            paginas.cuerpo = datos['cuerpo']
            paginas.autor = datos['autor']
            paginas.fecha = datos['fecha']            
            paginas.save()

            paginas = Posteo.objects.all()
            print (paginas)
            return render (request,'paginas.html',{"paginas":paginas})
        else:
            texto = f"algunos campos contienen errores"
            #return HttpResponse(texto)
            return render (request, 'paginas.html', {'paginas':paginas, 'texto':texto})
    else: 
        
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        formulario = Pagina_formulario(initial={'titulo':paginas.titulo,'subtitulo':paginas.subtitulo,'pelicula':paginas.pelicula,'cuerpo':paginas.cuerpo, 'autor':paginas.autor})
        
    
    return render (request,'form_editar_post.html', {'formulario':formulario,'paginas':paginas,'fecha':fecha})


def editar_imagen (request, id):
    imagen = Posteo.objects.get(id=id)

    if request.method == 'POST':
        formulario = Editar_Imagen(request.POST,request.FILES)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            imagen.imagen = datos['imagen']
            imagen.save()

            paginas = Posteo.objects.all()
            return render(request,'paginas.html',{'paginas':paginas})
        else:
            texto = f'la imagen no es de un formato valido'
            paginas = Posteo.objects.all()
            return render(request,'paginas.html',{'paginas':paginas,'texto':texto})

    else: 
                
        formulario = Pagina_formulario(initial={'imagen':imagen.imagen})

    return render (request,'editar_imagen_post.html', {'formulario':formulario,'imagen':imagen})



def login_request (request):

    if request.method == 'POST':
        formulario = Login_formulario(request, data=request.POST)

        if formulario.is_valid():
            usuario = formulario.cleaned_data.get('username')
            contrasenia = formulario.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request,user)
                avatares = Avatar.objects.filter(user=request.user.id)
                if avatares:                                  
                    return render (request,'inicio.html', {'avatar':avatares[0].imagen.url})
                else:
                    no_avatar =   '/static/Blog/assets/img/noavatar.webp'
                    return render (request,'inicio.html', {'avatar':no_avatar})
            else:
                return render (request,'login.html',{'mensaje':"Error. Fomulario erroneo."})    

        else:
            formulario = Login_formulario()
            return render (request, 'login.html', {'formulario':formulario, 'mensaje': "Error. Datos de ingreso incorrectos"})

    formulario = Login_formulario()        

    return render (request, 'login.html',{'formulario':formulario})


def register (request):

    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = RegisterUserForm(request.POST)
        

        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()

            return render(request,'inicio.html',{'mensaje':'Usuario Creado'})    

       
    else:
        #form = UserCreationForm()
        form = RegisterUserForm(request.POST)       

    return render (request, 'register.html',{'form':form})
         


def logout_usuario (request):
    logout(request)

    return redirect ('Login')


def editar_usuario (request):

    usuario = request.user

    if request.method == 'POST':
        formulario = Editar_Usuario_Form(request.POST)

        if formulario.is_valid():
             datos = formulario.cleaned_data

             usuario.email = datos['email']
             contrasenia = datos['password1']
             usuario.setpassword = contrasenia
             usuario.first_name = datos['first_name']
             usuario.last_name = datos['last_name']
             usuario.save()

             return render (request,'paginas.html',{'msg_edit_usuario':'datos actualizados'})
        
    else:
        formulario = Editar_Usuario_Form(initial={'email':usuario.email,'first_name':usuario.first_name,'last_name':usuario.last_name})


    return render (request, 'editar_usuario.html', {'formulario':formulario,'usuario':usuario})


def editar_avatar(request, id):

    usuario = request.user.id    

    if request.method == "POST":
        formulario = Avatar_Formulario(request.POST, request.FILES)

        if formulario.is_valid():            
            avatar = Avatar (imagen=formulario.cleaned_data['imagen'])
            avatar.save()
            return render(request,'inicio.html')
    
    else:
        formulario = Avatar_Formulario()    

    return render (request,'editar_avatar.html',{'formulario':formulario})





