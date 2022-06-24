from queue import Empty
from time import strftime
from urllib import request
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


def inicio (request):    
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    archivos_pelis = ['image1.jpg',
                'image2.jpg',
                'image3.jpg',
                'image4.jpg',
                'image5.jpg',
                'image6.jpg',
                'image7.jpg',
                'image8.jpg',
                'image9.jpg',
                'image10.jpg'
                ]
    archivos_series = [
        'imgseries01.jpg',
        'imgseries02.jpg',
        'imgseries03.jpg',
        'imgseries04.jpg',
        'imgseries05.jpg',
        'imgseries06.jpg',
        'imgseries07.jpg',
        'imgseries08.jpg',
        'imgseries09.jpg',
        'imgseries10.jpg',
    ]
    portada = random.choice(archivos_pelis)
    portada_series = random.choice(archivos_series) 
    
    return render (request,'inicio.html', {'avatar':avatar,'portada':portada,'portada_series':portada_series})


def paginas (request):
    paginas = Posteo.objects.all()       
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
                                     
    return render (request,'paginas.html', {'avatar':avatar,'paginas':paginas})


@login_required
def pagina_single(request, id):   

    pagina = Posteo.objects.get(id=id)
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    autor = request.user.username
    mensajes = Mensaje.objects.filter(id_clase=id, clase='pagina')
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if request.method == 'POST':  #Crea los mensajes para cada pagina individual
        formulario = Mensaje_formulario(request.POST, request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data
            mensaje = Mensaje(autor = datos['autor'],
                              fecha = datos['fecha'],
                              comentario = datos['comentario'],
                              id_clase=datos['id_clase'],
                              pelicula = datos['pelicula'],
                              clase = datos['clase']
                              )
            mensaje.save()
        else:
            msg_vacio = f"¡debes escribir algo!"
            return render (request,'pagina.html', {'pagina':pagina,
                                    'avatar':avatar,
                                    'mensajes':mensajes,
                                    'autor':autor,
                                    'fecha':fecha,
                                    'msg_vacio':msg_vacio
                                    })  
                                      
    return render (request,'pagina.html', {'pagina':pagina,
                                           'avatar':avatar,
                                           'mensajes':mensajes,
                                           'autor':autor,
                                           'fecha':fecha}
                                           )


def peliculas (request):
    peliculas = Pelicula.objects.all()
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    
    return render (request,'peliculas.html', {'peliculas':peliculas,'avatar':avatar})
    


def pelicula_single(request, id):   

    pelicula = Pelicula.objects.get(id=id)
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    autor = request.user.username
    mensajes = Mensaje.objects.filter(id_clase=id, clase='pelicula')
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     

    if request.method == 'POST':
        formulario = Mensaje_formulario(request.POST, request.FILES)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            mensaje = Mensaje(autor = datos['autor'],
                              fecha = datos['fecha'],
                              comentario = datos['comentario'],
                              id_clase=datos['id_clase'],
                              pelicula = datos['pelicula'],
                              clase = datos['clase']
                              )
            mensaje.save()
        else:
            msg_vacio = f"¡debes escribir algo!"
            return render (request,'pelicula.html', {'pelicula':pelicula,
                                    'avatar':avatar,
                                    'mensajes':mensajes,
                                    'autor':autor,
                                    'fecha':fecha,
                                    'msg_vacio':msg_vacio
                                    }) 
                                      
    return render (request,'pelicula.html', {'pelicula':pelicula,
                                             'avatar':avatar,
                                             'mensajes':mensajes,
                                             'autor':autor,
                                             'fecha':fecha
                                             })
    

@login_required
def pelicula_borrar(request, id):
    mensajes = Mensaje.objects.filter(id_clase=id,clase="pelicula")
    mensajes.delete()
    pelicula = Pelicula.objects.get(id=id)
    pelicula.delete()
    peliculas = Pelicula.objects.all()
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
                                 
    return render (request,'peliculas.html', {'peliculas':peliculas,'avatar':avatar})
   

@login_required
def editar_pelicula(request, id):
    pelicula = Pelicula.objects.get(id=id)
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    

    if request.method == 'POST':
        formulario = Editar_Pelicula_Formulario(request.POST)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            pelicula.nombre = datos['nombre']
            pelicula.trama_breve = datos['trama_breve']
            pelicula.trama_larga = datos['trama_larga']
            pelicula.anio = datos['anio']
            pelicula.save()

            return redirect('pelicula_single', id)
        else:
            alerta = f'Todos los campos deben estar completados'
            formulario = Editar_Pelicula(initial={'nombre':pelicula.nombre,
                                              'trama_breve':pelicula.trama_breve,
                                              'trama_larga':pelicula.trama_larga,
                                              'anio':pelicula.anio
                                              })
            return render (request,'form_editar_pelicula.html', {'formulario':formulario,
                                                         'pelicula':pelicula,
                                                         'avatar':avatar,
                                                         'alerta':alerta
                                                         })

    else:         
        formulario = Editar_Pelicula(initial={'nombre':pelicula.nombre,
                                              'trama_breve':pelicula.trama_breve,
                                              'trama_larga':pelicula.trama_larga,
                                              'anio':pelicula.anio
                                              }) 
                                      
    return render (request,'form_editar_pelicula.html', {'formulario':formulario,
                                                         'pelicula':pelicula,
                                                         'avatar':avatar
                                                         })
    

@login_required
def editar_imagen_pelicula(request, id):
    imagen = Pelicula.objects.get(id=id)
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))

    if request.method == 'POST':
        formulario = Editar_Imagen(request.POST, request.FILES)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            imagen.imagen=datos['imagen']
            imagen.save()
              
            return redirect ('pelicula_single', id) 
                                      
    return render (request,'editar_imagen_pelicula.html', {'imagen':imagen,'avatar':avatar})    


@login_required
def alta_pelicula (request):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    autor = request.user.username
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if request.method == 'POST':
        formulario = Pelicula_formulario(request.POST, request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data            
            pelicula = Pelicula(nombre = datos['nombre'],
                                trama_breve = datos['trama_breve'],
                                trama_larga = datos['trama_larga'],
                                anio = datos['anio'],
                                imagen = datos['imagen'],
                                autor = datos['autor'],
                                fecha = datos['fecha']
                                )
            pelicula.save()            
            peliculas = Pelicula.objects.all()
                                  
            return render (request,'peliculas.html', {'peliculas':peliculas,'avatar':avatar})
        else:
            texto = f"error en uno de los campos"
            return render (request,'alta_peliculas.html',{'texto':texto,'avatar':avatar})
    
    formulario = Pelicula_Crear()                                  
    return render (request,'alta_peliculas.html',{'avatar':avatar,
                                                  'formulario':formulario,
                                                  'autor':autor,
                                                  'fecha':fecha
                                                  })
    

@login_required
def eliminar_mensaje (request,id):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    mensaje = Mensaje.objects.get(id=id)
    mensaje.delete()
    peliculas = Pelicula.objects.all()
    series = Serie.objects.all()
    paginas = Posteo.objects.all()
    mensajes = Mensaje.objects.all()
    tipo_usuario = request.user.is_staff

    if tipo_usuario == 1:
         return render (request,'panel.html', {'avatar':avatar,
                                               'peliculas':peliculas,
                                               'series':series,
                                               'paginas':paginas,
                                               'mensajes':mensajes
                                               })
    else:
        datos = request.user        
        usuario = request.user.username
        paginas = Posteo.objects.filter(autor=request.user.username)
        mensajes = Mensaje.objects.filter(autor=request.user.username)
        series = Serie.objects.filter(autor=request.user.username)
        
                                        
        return render (request,'perfil.html', {'avatar':avatar,
                                               'paginas':paginas,
                                               'datos':datos,
                                               'mensajes':mensajes,
                                               'usuario':usuario,
                                               'series':series
                                               })
    

@login_required
def editar_mensaje (request,id):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    comentario = Mensaje.objects.get(id=id)

    if request.method == 'POST':
        formulario = Editar_Mensaje_formulario(request.POST)
        if formulario.is_valid():
            datos_msg = formulario.cleaned_data
            comentario.fecha = datos_msg['fecha']
            comentario.editado = datos_msg['editado']
            comentario.comentario = datos_msg['comentario']
            comentario.save()
            
            usuario = request.user.id

            return redirect('perfil',usuario)                                  
            
        else:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            texto = f'error en el formulario'
            return render(request,'form_editar_mensaje.html.html',{'texto':texto,'avatar':avatar,'fecha':fecha,'comentario':comentario})
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                      
    return render (request,'form_editar_mensaje.html',{'fecha':fecha,
                                                       'avatar':avatar,
                                                       'comentario':comentario
                                                       })


def buscar_mensajes (request):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    pelicula = Pelicula.objects.all()
    pagina = Posteo.objects.all()
    texto = f'Ingrese un texto en el campo de búsqueda'

    if request.GET['autor']:
        autor = request.GET['autor']
        mensajes = Mensaje.objects.filter(autor__icontains=autor)
        texto2 = f'no se han encontrado comentarios hechos por "{autor}"'

        if mensajes:                                   
            return render (request,'res_busc_mensaje.html',{'mensajes':mensajes,
                                                            'avatar':avatar,
                                                            'pagina':pagina,
                                                            'pelicula':pelicula,
                                                            'autor':autor})
        else:                       
            return render (request,'res_busc_mensaje.html',{'mensajes':mensajes,
                                                            'avatar':avatar,
                                                            'pagina':pagina,
                                                            'pelicula':pelicula,
                                                            'autor':autor,
                                                            'texto2':texto2
                                                            })   
    else:                      
        return render (request,'res_busc_mensaje.html',{'avatar':avatar,
                                                        'pagina':pagina,
                                                        'pelicula':pelicula,
                                                        'texto':texto
                                                        })
        

@login_required
def alta_pagina (request):    
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))    
    
    if request.method == 'POST':
        formulario = Pagina_formulario(request.POST,request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data
            pagina = Posteo(titulo = datos['titulo'],
                            subtitulo = datos['subtitulo'],
                            pelicula = datos['pelicula'],
                            cuerpo = datos['cuerpo'],
                            autor = datos['autor'],
                            fecha = datos['fecha'],
                            imagen = datos['imagen']
                            )
            pagina.save()
            texto3 = f'Post creado con exito'
            paginas = Posteo.objects.all()

            return render(request,'paginas.html',{'texto3':texto3,
                                                  'avatar':avatar,
                                                  'paginas':paginas
                                                  })
        else:
            texto = f'error en uno de los campos'
            return render(request,'alta_paginas.html',{'texto':texto,'avatar':avatar})
           
    formulario = Pagina_Crear() 
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usuario = request.user.username
                                  
    return render (request,'alta_paginas.html',{'avatar':avatar,
                                                'fecha':fecha,
                                                'usuario':usuario,
                                                'formulario':formulario
                                                })


def buscar_pelicula(request):    
        avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))

        if request.GET['nombre']:
            nombre = request.GET['nombre']
            peliculas = Pelicula.objects.filter(nombre__icontains=nombre)
            
            if peliculas:
                return render (request,'res_busc_peli.html', {'peliculas':peliculas,
                                                              'peli':nombre,
                                                              'avatar':avatar
                                                              })
            else:
                peliculas = Pelicula.objects.all()
                texto2 = f'no se han encontrado peliculas conteniendo "{nombre}"'
                return render (request,'peliculas.html', {"peliculas":peliculas,
                                                          "texto2":texto2,
                                                          'avatar':avatar
                                                          })
        else:
            peliculas = Pelicula.objects.all()
            texto = f'Ingrese un texto en el campo de búsqueda'
            return render (request,'peliculas.html', {"peliculas":peliculas,
                                                      "texto":texto,
                                                      'avatar':avatar
                                                      })
       

def buscar_pagina (request):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))

    if request.GET['pelicula']:
            nombre = request.GET['pelicula']
            paginas = Posteo.objects.filter(pelicula__icontains=nombre)

            if paginas:
                return render (request,'res_busc_pagina.html', {'paginas':paginas,
                                                                'nombre':nombre,
                                                                'avatar':avatar
                                                                })
            else:
                paginas = Posteo.objects.all()
                texto2 = f'no se han encontrado peliculas conteniendo "{nombre}"'
                return render (request,'paginas.html', {"paginas":paginas,
                                                        "texto2":texto2,
                                                        'avatar':avatar
                                                        })   
    else:
        paginas = Posteo.objects.all()
        texto = f'Ingrese un texto en el campo de búsqueda'
        return render (request,'paginas.html', {"paginas":paginas,
                                                "texto":texto,
                                                'avatar':avatar
                                                })


@login_required
def eliminar_pagina(request, id):
        avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
        mensajes = Mensaje.objects.filter(id_clase=id,clase="pagina")
        mensajes.delete()
        pagina = Posteo.objects.get(id=id)
        pagina.delete()
        paginas = Posteo.objects.all()

        return render (request,'paginas.html',{"paginas":paginas,'avatar':avatar})


@login_required
def editar_pagina (request, id):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
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
            paginas.editado = datos['editado']            
            paginas.save()

            paginas = Posteo.objects.all()
            autor = request.user.username
            mensajes = Mensaje.objects.filter(id_clase=id, clase='pagina')
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            datos = request.user           
            
            return redirect ('pagina_single', id)
           
        else:
            texto = f"algunos campos contienen errores"
            pagina = Posteo.objects.get(id=id)
            autor = request.user.username
            mensajes = Mensaje.objects.filter(id_clase=id, clase='pagina')
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            return render (request, 'form_editar_pagina.html', {'pagina':pagina,
                                                                'texto':texto,
                                                                'avatar':avatar,
                                                                'mensajes':mensajes,
                                                                'autor':autor,
                                                                'fecha':fecha
                                                                })
    formulario = Editar_Pagina(initial={'titulo':paginas.titulo,
                                        'subtitulo':paginas.subtitulo,
                                        'pelicula':paginas.pelicula,
                                        'cuerpo':paginas.cuerpo
                                        })
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    usuario = request.user.username

    return render (request,'form_editar_pagina.html', {'paginas':paginas,
                                                       'fecha':fecha,
                                                       'usuario':usuario,
                                                       'avatar':avatar,
                                                       'formulario':formulario
                                                       })


@login_required
def editar_imagen_pagina (request, id):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    imagen = Posteo.objects.get(id=id)

    if request.method == 'POST':
        formulario = Editar_Imagen(request.POST,request.FILES)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            imagen.imagen = datos['imagen']
            imagen.save()
            
            return redirect ('pagina_single', id)
            
        else:
            texto = f'la imagen no es de un formato valido'
            pagina = Posteo.objects.get(id=id)
            return render(request,'pagina.html',{'pagina':pagina,
                                                 'texto':texto,
                                                 'avatar':avatar
                                                 })
    else:        
        formulario = Pagina_formulario(initial={'imagen':imagen.imagen})

    return render (request,'editar_imagen_pagina.html', {'formulario':formulario,
                                                         'imagen':imagen,
                                                         'avatar':avatar
                                                         })


@login_required
def perfil (request, id):

    datos = request.user
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    usuario = request.user.username
    paginas = Posteo.objects.filter(autor=request.user.username)
    mensajes = Mensaje.objects.filter(autor=request.user.username)
    series = Serie.objects.filter(autor=request.user.username)
    foto_perfil = request.user.id
    verificacion = len (Avatar.objects.filter(user=request.user.id))

    if verificacion > 0:
        return render (request,'perfil.html',{'avatar':avatar,
                                                'paginas':paginas,
                                                'datos':datos,
                                                'mensajes':mensajes,
                                                'usuario':usuario,
                                                'series':series,
                                                'foto_perfil':foto_perfil
                                           })
    else:
        return render (request,'perfil.html',{'avatar':avatar,
                                                'paginas':paginas,
                                                'datos':datos,
                                                'mensajes':mensajes,
                                                'usuario':usuario,
                                                'series':series,                                                
                                           })
    

@login_required
def panel (request):
    peliculas = Pelicula.objects.all()
    series = Serie.objects.all()
    paginas = Posteo.objects.all()
    mensajes = Mensaje.objects.all()
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))    

    return render (request,'panel.html',{'peliculas':peliculas,
                                         'paginas':paginas,
                                         'mensajes':mensajes,
                                         'avatar':avatar,
                                         'series':series
                                         })
    

def acerca(request):
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))    
    return render (request,'acerca.html',{'avatar':avatar})






def series (request):
    series = Serie.objects.all()
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    vacio = f'No hay series para mostrar aun'
    
    return render (request,'series.html', {'series':series,'avatar':avatar, 'vacio':vacio})
    


def serie_single(request, id):   

    serie = Serie.objects.get(id=id)
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    autor = request.user.username
    mensajes = Mensaje.objects.filter(id_clase=id, clase='serie')
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     

    if request.method == 'POST':
        formulario = Mensaje_formulario(request.POST, request.FILES)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            mensaje = Mensaje(autor = datos['autor'],
                              fecha = datos['fecha'],
                              comentario = datos['comentario'],
                              id_clase=datos['id_clase'],
                              pelicula = datos['pelicula'],
                              clase = datos['clase']
                              )
            mensaje.save()
        else:
            msg_vacio = f"¡debes escribir algo!"            
            return render (request,'serie.html', {'serie':serie,
                                    'avatar':avatar,
                                    'mensajes':mensajes,
                                    'autor':autor,
                                    'fecha':fecha,
                                    'msg_vacio':msg_vacio
                                    }) 
                                      
    return render (request,'serie.html', {'serie':serie,
                                             'avatar':avatar,
                                             'mensajes':mensajes,
                                             'autor':autor,
                                             'fecha':fecha
                                             })


@login_required
def alta_serie (request):  #corregir
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
    autor = request.user.username
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if request.method == 'POST':
        formulario = Serie_formulario(request.POST, request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data            
            serie = Serie(nombre = datos['nombre'],
                                resumen = datos['resumen'],
                                trama = datos['trama'],
                                anio = datos['anio'],
                                imagen = datos['imagen'],
                                autor = datos['autor'],
                                fecha = datos['fecha']
                                )
            serie.save()            
            series = Serie.objects.all()
                                  
            return render (request,'series.html', {'series':series,'avatar':avatar})
        else:
            texto = f"error en uno de los campos"
            return render (request,'alta_series.html',{'texto':texto,'avatar':avatar})
    
    formulario = Serie_Crear()                                  
    return render (request,'alta_series.html',{'avatar':avatar,
                                                  'formulario':formulario,
                                                  'autor':autor,
                                                  'fecha':fecha
                                                  })

@login_required
def eliminar_serie (request, id):
    
    mensajes = Mensaje.objects.filter(id_clase=id,clase="serie")
    mensajes.delete()
    serie = Serie.objects.get(id=id)
    serie.delete()
    series = Serie.objects.all()
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))
                                 
    return render (request,'series.html', {'series':series,'avatar':avatar})
   

@login_required
def editar_serie(request, id): #corregir
    serie = Serie.objects.get(id=id)
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))

    if request.method == 'POST':
        formulario = Editar_Serie_Formulario(request.POST)

        if formulario.is_valid():
            datos = formulario.cleaned_data
            serie.nombre = datos['nombre']
            serie.resumen = datos['resumen']
            serie.trama = datos['trama']
            serie.anio = datos['anio']
            serie.save()

            return redirect('serie_single', id)
        else:
            alerta = f'Todos los campos deben estar completados'
            formulario = Editar_Serie(initial={'nombre':serie.nombre,
                                              'resumen':serie.resumen,
                                              'trama':serie.trama,
                                              'anio':serie.anio
                                              })
            return render (request,'form_editar_serie.html', {'formulario':formulario,
                                                         'serie':serie,
                                                         'avatar':avatar,
                                                         'alerta':alerta
                                                         })
    else:         
        formulario = Editar_Serie(initial={'nombre':serie.nombre,
                                              'resumen':serie.resumen,
                                              'trama':serie.trama,
                                              'anio':serie.anio
                                              }) 
                                      
    return render (request,'form_editar_serie.html', {'formulario':formulario,
                                                         'serie':serie,
                                                         'avatar':avatar
                                                         })
    

@login_required
def editar_imagen_serie(request, id):  #corregir
    imagen = Serie.objects.get(id=id)
    avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))

    if request.method == 'POST':
        formulario = Editar_Imagen(request.POST, request.FILES)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            imagen.imagen=datos['imagen']
            imagen.save()
              
            return redirect ('serie_single', id) 
                                      
    return render (request,'editar_imagen_serie.html', {'imagen':imagen,'avatar':avatar})    


def buscar_serie(request):    
        avatar = imagenAvatar(Avatar.objects.filter(user=request.user.id))

        if request.GET['nombre']:
            nombre = request.GET['nombre']
            series = Serie.objects.filter(nombre__icontains=nombre)
            
            if series:
                return render (request,'res_busc_serie.html', {'series':series,
                                                              'nombre':nombre,
                                                              'avatar':avatar
                                                              })
            else:
                series = Serie.objects.all()
                texto2 = f'no se han encontrado series conteniendo "{nombre}"'
                return render (request,'series.html', {"series":series,
                                                          "texto2":texto2,
                                                          'avatar':avatar
                                                          })
        else:
            series = Serie.objects.all()
            texto = f'Ingrese un texto en el campo de búsqueda'
            return render (request,'series.html', {"series":series,
                                                      "texto":texto,
                                                      'avatar':avatar
                                                      })

