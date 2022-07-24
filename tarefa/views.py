
from django.shortcuts import render, redirect
from usuarios.models import Usuario
from .models import Tarefas

def index(request):
    if request.session.get('usuario'):
        usuarioLogado = Usuario.objects.get(id = request.session['usuario'])
        tarefas = Tarefas.objects.filter(usuario= usuarioLogado)
        print(tarefas[0].data_compromisso)
        return render(request, 'index.html', {'tarefas': tarefas })
    else:
        return redirect('/auth/login/?status=3')