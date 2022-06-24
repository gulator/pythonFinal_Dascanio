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

def imagenAvatar(a,**kwargs):
    avatares = a
    if avatares:                                  
        return (avatares[0].imagen.url)
    else:
        no_avatar = '/static/Blog/assets/img/noavatar.webp'
        return (no_avatar)


def login_request (request):
    
    archivos_pelis = ['image1.jpg','image2.jpg','image3.jpg','image4.jpg','image5.jpg','image6.jpg','image7.jpg','image8.jpg','image9.jpg','image10.jpg']
    archivos_series = ['imgseries01.jpg','imgseries02.jpg','imgseries03.jpg','imgseries04.jpg','imgseries05.jpg','imgseries06.jpg','imgseries07.jpg','imgseries08.jpg','imgseries09.jpg','imgseries10.jpg']
    portada = random.choice(archivos_pelis)
    portada_series = random.choice(archivos_series)
    
    if request.method == 'POST':
        
        formulario = Login_formulario(request, data=request.POST)

        if formulario.is_valid():
            usuario = formulario.cleaned_data.get('username')
            contrasenia = formulario.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request,user)
                avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))                                     
                return render (request,'inicio.html',{'avatar':avatar,'portada':portada,'portada_series':portada_series})                
            else:
                return render (request,'login.html',{'mensaje':"Error. Formulario erroneo."})    

        else:
            formulario = Login_formulario()
            return render (request, 'login.html', {'formulario':formulario, 'mensaje': "Error. Datos de ingreso incorrectos"})

    formulario = Login_formulario()        

    return render (request, 'login.html',{'formulario':formulario})


def register (request):

    archivos = ['image1.jpg','image2.jpg','image3.jpg','image4.jpg','image5.jpg','image6.jpg','image7.jpg','image8.jpg','image9.jpg','image10.jpg']
    portada = random.choice(archivos)

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            return render (request,'inicio.html',{'usuario_creado':'Usuario Creado. Proceda con el login','portada':portada})   
    else:
        form = RegisterUserForm(request.POST)  

    return render (request, 'register.html',{'form':form})
         


def logout_usuario (request):
    logout(request)

    return redirect ('inicio')

@login_required
def editar_usuario (request):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    usuario = request.user
    paginas = Posteo.objects.filter(autor=request.user.username)
    nombre_usuario = request.user.username
    mensajes = Mensaje.objects.filter(autor=request.user.username)

    if request.method == 'POST':
        formulario = Editar_Usuario_Form(request.POST)

        if formulario.is_valid():
                datos = formulario.cleaned_data
                usuario.email = datos['email']
                usuario.first_name = datos['first_name']
                usuario.last_name = datos['last_name']
                usuario.save()
                datos = request.user
                usuario = request.user.username
                id = request.user.id
                return redirect('perfil',id)
        else:
            documento = {'avatar':avatar,
                         'usuario':nombre_usuario,
                         'paginas':paginas,
                         'datos':usuario,
                         'mensajes':mensajes,
                         'msg_edit_usuario_error':'¡datos invalidos!'
                        }

            return render (request,'perfil.html',documento)
    else:
        datos = request.user
        avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
        usuario = request.user.username
        paginas = Posteo.objects.filter(autor=request.user.username)
                                  
        return render (request,'perfil.html', {'avatar':avatar,
                                               'mensajes':mensajes,
                                               'paginas':paginas,
                                               'datos':datos,
                                               'usuario':usuario,})

def borrar_avatar (request, id):
    avatar = Avatar.objects.filter(user_id=id)
    avatar.delete()

    return redirect('perfil',id)

@login_required
def editar_avatar(request):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))    

    if request.method == "POST":
        formulario = Avatar_Formulario(request.POST, request.FILES)

        if formulario.is_valid():
            usuario = request.user.id
            imagen = Avatar.objects.filter(user_id=usuario)
            id = imagen[0].id
            cambio = Avatar.objects.get(id=id)
            avatar = formulario.cleaned_data                 
            cambio.imagen = avatar['imagen']            
            cambio.save()
            datos = request.user
            avatares = Avatar.objects.filter(user=request.user.id)
            usuario = request.user.username
            paginas = Posteo.objects.filter(autor=request.user.username)
            mensajes = Mensaje.objects.filter(autor=request.user.username)
            id_usuario = request.user.id

            return redirect ('perfil', id_usuario)
                                                
            #return render (request,'perfil.html', {'avatar':avatares[0].imagen.url,'paginas':paginas,'datos':datos,'mensajes':mensajes,'usuario':usuario,})
        else:
            formulario = Avatar_Formulario()
        
        return render (request,'editar_avatar.html')
    
    avatares = Avatar.objects.filter(user=request.user.id)
    
    if len (avatares)>0:
        avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id)) 
        return render(request,'editar_avatar.html',{'avatar':avatar})
    else:
        usuario = request.user.id
        imagenes = Avatar (imagen="avatares/noavatar.webp",user_id=usuario)
        imagenes.save()
        imagen = Avatar.objects.get(user_id=usuario)             
        return render (request,'editar_avatar.html',{'avatar':avatar})


def cambiar_password(request):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    usuario = request.user

    if request.method == 'POST':
        formulario = CambiarPassword(request.POST)

        if formulario.is_valid():
            datos = formulario.cleaned_data            

            if datos['password1'] == datos['password2']:
                contrasenia = datos['password1']
                usuario.set_password(contrasenia)
                datos = request.user
                usuario = request.user.username
                paginas = Posteo.objects.filter(autor=request.user.username)
                mensajes = Mensaje.objects.filter(autor=request.user.username)

                return render (request,'perfil.html', {'avatar':avatar,
                                                    'paginas':paginas,
                                                    'datos':datos,
                                                    'mensajes':mensajes,
                                                    'usuario':usuario,
                                                    'msg_edit_usuario':'Contraseña Actualizada'
                                                    })
            else:
                return render (request, 'cambiar_password.html',{'avatar':avatar,'msg_edit_usuario_error':'Las contraseñas no coinciden'})                                            
        else:            
            return render (request, 'cambiar_password.html',{'avatar':avatar,'msg_edit_usuario_error':'contraseña invalida'})
    
    else:
        formulario = CambiarPassword()
        return render (request, 'cambiar_password.html',{'avatar':avatar,'formulario':formulario})

