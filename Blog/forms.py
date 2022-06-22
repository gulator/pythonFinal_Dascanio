from dataclasses import fields
from logging import PlaceHolder
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Pelicula, Posteo
from ckeditor.fields import RichTextField,RichTextFormField


class Pelicula_formulario(forms.Form):
    nombre = forms.CharField(max_length=60)
    trama_breve = forms.CharField(max_length=250,widget=forms.Textarea)
    trama_larga = forms.CharField(widget=forms.Textarea)
    anio = forms.IntegerField()
    imagen = forms.ImageField()

class Pelicula_Crear(forms.ModelForm):

    nombre = forms.CharField(max_length=60, label=('Nombre de la pelicula:'), widget=forms.TextInput(attrs={'class':'form-control'}))
    trama_breve = forms.CharField(max_length=250, label=('Resumen:'), widget=forms.Textarea(attrs={'class':'form-control','rows':"4"}))    
    anio = forms.IntegerField(label=('Año:'), widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model = Pelicula
        fields = ('nombre', 'trama_breve', 'trama_larga', 'anio', 'imagen')   
    Widget = {
        'trama_larga' : forms.Textarea(attrs={'class': 'form-control'})
    }

class Editar_Pelicula(forms.ModelForm):

    nombre = forms.CharField(max_length=60, label=('Nombre de la pelicula:'), widget=forms.TextInput(attrs={'class':'form-control'}))
    trama_breve = forms.CharField(max_length=250, label=('Resumen:'), widget=forms.Textarea(attrs={'class':'form-control','rows':"4"}))    
    anio = forms.IntegerField(label=('Año:'), widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model = Pelicula
        fields = ('nombre', 'trama_breve', 'trama_larga', 'anio')   
    Widget = {
        'trama_larga' : forms.Textarea(attrs={'class': 'form-control'})
    }    

class Editar_Pelicula_Formulario(forms.Form):
    nombre = forms.CharField(max_length=60)
    trama_breve = forms.CharField(max_length=250, widget=forms.Textarea)
    trama_larga = forms.CharField (widget=forms.Textarea)
    anio = forms.IntegerField()


class Mensaje_formulario(forms.Form):
    autor = forms.CharField(max_length=60)
    fecha = forms.DateTimeField()    
    comentario = forms.CharField(widget=forms.Textarea)
    id_clase = forms.IntegerField()
    clase = forms.CharField(max_length=10)
    pelicula = forms.CharField(max_length=60)


class Editar_Mensaje_formulario(forms.Form):
    
    fecha = forms.DateTimeField()    
    comentario = forms.CharField(widget=forms.Textarea)    
    editado = forms.CharField(max_length=10)


class Pagina_formulario(forms.Form):
    titulo = forms.CharField(max_length=80)
    subtitulo = forms.CharField(max_length=80)
    pelicula = forms.CharField(max_length=60)
    cuerpo = forms.CharField (widget=forms.Textarea)    
    autor = forms.CharField(max_length=40)
    fecha = forms.DateTimeField()
    imagen = forms.ImageField()

class Pagina_Crear(forms.ModelForm):
    class Meta:
        model = Posteo
        fields = ('titulo', 'subtitulo','pelicula','cuerpo','imagen')

        widgets = {
            'titulo' : forms.TextInput(attrs={'class': 'form-control'}),
            'subtitulo' : forms.TextInput(attrs={'class': 'form-control'}),
            'pelicula' : forms.TextInput(attrs={'class': 'form-control'}),
            'cuerpo' : forms.Textarea(attrs={'class': 'form-control'}),            

        }


class Editar_Pagina_formulario(forms.Form):
    titulo = forms.CharField(max_length=80)
    subtitulo = forms.CharField(max_length=80)
    pelicula = forms.CharField(max_length=60)
    cuerpo = forms.CharField (widget=forms.Textarea)    
    autor = forms.CharField(max_length=40)
    fecha = forms.DateTimeField()
    editado = forms.CharField(max_length=10)

class Editar_Pagina(forms.ModelForm):
    class Meta:
        model = Posteo
        fields = ('titulo', 'subtitulo','pelicula','cuerpo')

        widgets = {
            'titulo' : forms.TextInput(attrs={'class': 'form-control'}),
            'subtitulo' : forms.TextInput(attrs={'class': 'form-control'}),
            'pelicula' : forms.TextInput(attrs={'class': 'form-control'}),
            'cuerpo' : forms.Textarea(attrs={'class': 'form-control'}),           
        }
        

class Editar_Imagen(forms.Form):    
    imagen = forms.ImageField()


class RegisterUserForm (UserCreationForm):

    email = forms.EmailField(label='Mail', widget=forms.EmailInput(attrs={'class':'form-control','Style':'width: 300px','placeholder':'Ej: mail@mail.com'}))
    password1 = forms.CharField(label=('Contraseña'), widget=forms.PasswordInput(attrs={'class':'form-control','Style':'width: 300px','placeholder':'ingrese una contraseña'}))
    password2 = forms.CharField(label=('Confirmar'), widget=forms.PasswordInput(attrs={'class':'form-control','Style':'width: 300px','placeholder':'repita la contraseña'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {k:"" for k in fields}    
      

    def __init__(self, *args, **kwargs):
            super(UserCreationForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] ='form-control'
            self.fields['username'].widget.attrs['placeholder'] ='elija su usuario'


class Login_formulario (AuthenticationForm):    

    class Meta:
        model = User
        fields = ['username', 'password']

class Editar_Usuario_Form (UserCreationForm):

    first_name = forms.CharField(label=('Nombre'), required=False, widget=forms.TextInput(attrs={'class':'form-control','Style':'width: 300px'}))
    last_name = forms.CharField(label=('Apellido'), required=False, widget=forms.TextInput(attrs={'class':'form-control','Style':'width: 300px'}))
    email = forms.EmailField(label='Mail', required=False, widget=forms.EmailInput(attrs={'class':'form-control','Style':'width: 300px'}))
    password1 = forms.CharField(label=('Contraseña'), required=False, widget=forms.PasswordInput(attrs={'class':'form-control','Style':'width: 300px'}))
    password2 = forms.CharField(label=('Confirmar'), required=False, widget=forms.PasswordInput(attrs={'class':'form-control','Style':'width: 300px'}))

    class Meta:
        model = User
        fields = ['email','password1','password2','first_name','last_name']
        help_texts = {k:"" for k in fields}  

class Avatar_Formulario(forms.Form):
    
    imagen = forms.ImageField()
    
    

