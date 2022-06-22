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
    
    archivos = ['image1.jpg','image2.jpg','image3.jpg','image4.jpg','image5.jpg','image6.jpg','image7.jpg','image8.jpg','image9.jpg','image10.jpg']
    portada = random.choice(archivos)
    
    if request.method == 'POST':
        
        formulario = Login_formulario(request, data=request.POST)

        if formulario.is_valid():
            usuario = formulario.cleaned_data.get('username')
            contrasenia = formulario.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request,user)
                avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))                                     
                return render (request,'inicio.html',{'avatar':avatar,'portada':portada})                
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
            

            return render (request,'inicio.html',{'usuario_creado':'Usuario Creado','portada':portada})    

       
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

    if request.method == 'POST':
        formulario = Editar_Usuario_Form(request.POST)

        if formulario.is_valid():
            datos = formulario.cleaned_data            

            if datos['password1'] == datos['password2']:
                contrasenia = datos['password1']
                usuario.set_password(contrasenia)
                usuario.email = datos['email']
                usuario.first_name = datos['first_name']
                usuario.last_name = datos['last_name']
                usuario.save()

                datos = request.user
                avatares = Avatar.objects.filter(user=request.user.id)
                usuario = request.user.username
                posteos = Posteo.objects.filter(autor=request.user.username)
                                                 
                return render (request,'perfil.html', {'avatar':avatar,'posteos':posteos,'datos':datos,'usuario':usuario,'msg_edit_usuario':'Datos actualizados'})
                
            else:
                documento = {'avatar':avatar, 'usuario':usuario,'posteos':posteos,'datos':datos,'msg_edit_usuario_error':'Las contraseñas no coinciden'}
                return render (request,'perfil.html',documento)
        else:
            datos = request.user
            avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
            usuario = request.user.username
            posteos = Posteo.objects.filter(autor=request.user.username)
                                  
            return render (request,'perfil.html', {'avatar':avatar,'posteos':posteos,'datos':datos,'usuario':usuario,'msg_edit_usuario_error':'Las contraseñas no coinciden'})
         

@login_required
def editar_avatar(request):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))    

    if request.method == "POST":
        formulario = Avatar_Formulario(request.POST, request.FILES)

        if formulario.is_valid():
            id = imagen[0].id
            cambio = Avatar.objects.get(id=id)
            avatar = formulario.cleaned_data                 
            cambio.imagen = avatar['imagen']            
            cambio.save()

            datos = request.user
            avatares = Avatar.objects.filter(user=request.user.id)
            usuario = request.user.username
            posteos = Posteo.objects.filter(autor=request.user.username)
                                                
            return render (request,'perfil.html', {'avatar':avatares[0].imagen.url,'posteos':posteos,'datos':datos})

    
        else:
            formulario = Avatar_Formulario()
        
        return render (request,'editar_avatar.html')
    
    avatares = Avatar.objects.filter(user=request.user.id)
    
    if avatares:
        avatar = Avatar.objects.filter(user=request.user.id)  
        return render(request,'editar_avatar.html',{'avatar':avatar})

    else:
        usuario = request.user.id
        imagenes = Avatar (imagen="avatares/noavatar.webp",user_id=usuario)
        imagenes.save()
        imagen = Avatar.objects.get(user_id=usuario)             
        return render (request,'editar_avatar.html',{'avatar':avatar})