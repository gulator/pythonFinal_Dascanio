from urllib import request
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

path('inicio',views.inicio, name='inicio'),    
path('paginas', views.paginas, name='paginas'),
path('posteos', views.posteos, name='posteos'),
path('peliculas', views.peliculas,name='peliculas'),
path('pelicula_single/<int:id>', views.pelicula_single, name='pelicula_single'),
path('pelicula_borrar/<int:id>', views.pelicula_borrar, name='pelicula_borrar'),
path('editar_pelicula/<int:id>', views.editar_pelicula, name='editar_pelicula'),
path('pelicula_editar_imagen/<int:id>',views.pelicula_editar_imagen, name='pelicula_editar_imagen'),
path('mensajes', views.mensajes,name='mensajes'),
path('alta_pelicula', views.alta_pelicula,name='alta_pelicula'),
path('alta_mensaje', views.alta_mensaje,name='alta_mensaje'),
path('alta_pagina', views.alta_pagina,name='alta_pagina'),
path('busca_pelicula', views.busca_pelicula, name="busca_pelicula"),
path('buscar_pelicula', views.buscar_pelicula, name="buscar_pelicula"),
path('eliminar_post/<int:id>', views.eliminar_post, name="eliminar_post"),
path('editar_post/<int:id>', views.editar_post, name='editar_post'),
path('editar_imagen/<int:id>', views.editar_imagen, name='editar_imagen'),
path('editar_usuario', views.editar_usuario, name='editar_usuario'),
path('editar_avatar', views.editar_avatar, name='editar_avatar'),
path('login', views.login_request, name="Login"),
path('register', views.register, name="Register"),
path('logout', views.logout_usuario, name='Logout')

]