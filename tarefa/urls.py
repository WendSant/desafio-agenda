from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('edit/', views.edicao_Tarefa, name= 'edicao_Tarefa'),
    path('add/', views.add_Tarefa, name= 'add_Tarefa'),
    path('remove/', views.remove_Tarefa, name='remove_Tarefa')

]
