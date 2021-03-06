from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [

path('login', views.login_request, name="Login"),
path('register', views.register, name="Register"),
path('logout', views.logout_usuario, name='Logout'),
path('editar_usuario', views.editar_usuario, name='editar_usuario'),
path('editar_avatar', views.editar_avatar, name='editar_avatar'),
path('borrar_avatar/<int:id>', views.borrar_avatar, name='borrar_avatar'),
path('cambiar_password', views.cambiar_password, name='cambiar_password'),
]