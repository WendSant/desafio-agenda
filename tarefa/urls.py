from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('edit/', views.edicao_Tarefa, name= 'edicao_Tarefa')
]
