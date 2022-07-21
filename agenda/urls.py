from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('', include('usuarios.urls')),
    path('admin/', admin.site.urls),
    path('tarefa/', include('tarefa.urls')),
    path('auth/', include('usuarios.urls')),
]
