"""
URL configuration for traductor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from core.views import mostrar_html, signin, edit_user, historial, register, Salir

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signin, name='login'), #loginS
    path('registrar/', register, name='registrar'),
    path('salir/', Salir, name='salir'), #Go out
    path('inicio/', mostrar_html, name='inicio'), #home
    path('editar/', edit_user, name='editar'),
    path('historial/', historial, name='historial'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
