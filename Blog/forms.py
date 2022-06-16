from dataclasses import fields
from logging import PlaceHolder
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class Pelicula_formulario(forms.Form):
    nombre = forms.CharField(max_length=40)
    trama_breve = forms.CharField(max_length=250,widget=forms.Textarea)
    trama_larga = forms.CharField (widget=forms.Textarea)
    anio = forms.IntegerField()
    imagen = forms.ImageField()

class Editar_Pelicula_Formulario(forms.Form):
    nombre = forms.CharField(max_length=40)
    trama_breve = forms.CharField(max_length=250, widget=forms.Textarea)
    trama_larga = forms.CharField (widget=forms.Textarea)
    anio = forms.IntegerField()



class Mensaje_formulario(forms.Form):
    autor = forms.CharField(max_length=60)
    fecha = forms.DateTimeField()
    avatar = forms.ImageField(required=False)
    comentario = forms.CharField(widget=forms.Textarea)
    id_clase = forms.IntegerField()

class Pagina_formulario(forms.Form):
    titulo = forms.CharField(max_length=80)
    subtitulo = forms.CharField(max_length=80)
    pelicula = forms.CharField(max_length=70)
    cuerpo = forms.CharField (widget=forms.Textarea)    
    autor = forms.CharField(max_length=40)
    fecha = forms.DateTimeField()
    imagen = forms.ImageField()

class Editar_Pagina_formulario(forms.Form):
    titulo = forms.CharField(max_length=80)
    subtitulo = forms.CharField(max_length=80)
    pelicula = forms.CharField(max_length=70)
    cuerpo = forms.CharField (widget=forms.Textarea)    
    autor = forms.CharField(max_length=40)
    fecha = forms.DateTimeField()

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
    
    

