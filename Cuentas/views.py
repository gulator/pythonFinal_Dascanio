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
                return render (request,'login.html',{'mensaje':"Error. Formulario erroneo."})    

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

@login_required
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

@login_required
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