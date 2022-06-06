from django import forms

class Pelicula_formulario(forms.Form):
    nombre = forms.CharField(max_length=40)
    trama_breve = forms.CharField(max_length=250)
    trama_larga = forms.CharField (widget=forms.Textarea)
    anio = forms.IntegerField()
    imagen = forms.ImageField()

class Mensaje_formulario(forms.Form):
    autor = forms.CharField(max_length=60)
    fecha = forms.DateTimeField()
    avatar = forms.ImageField()
    comentario = forms.CharField(widget=forms.Textarea)

class Pagina_formulario(forms.Form):
    titulo = forms.CharField(max_length=80)
    subtitulo = forms.CharField(max_length=80)
    pelicula = forms.CharField(max_length=70)
    cuerpo = forms.CharField (widget=forms.Textarea)    
    autor = forms.CharField(max_length=40)
    fecha = forms.DateTimeField()
    imagen = forms.ImageField()

