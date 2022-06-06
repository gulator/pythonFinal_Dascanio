from django.urls import path
from . import views

urlpatterns = [
path('paginas', views.paginas, name='paginas'),
path('posteos', views.posteos, name='posteos'),
path('peliculas', views.peliculas,name='peliculas'),
path('mensajes', views.mensajes,name='mensajes'),
path('alta_pelicula', views.alta_pelicula,name='alta_pelicula'),
path('alta_mensaje', views.alta_mensaje,name='alta_mensaje'),
path('alta_pagina', views.alta_pagina,name='alta_pagina'),

]