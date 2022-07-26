import datetime

from django.utils.timezone import now, localtime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from usuarios.models import Usuario
from .models import Tarefas


def index(request):
    if request.session.get('usuario'):
        usuarioLogado = Usuario.objects.get(id=request.session['usuario'])
        tarefas = Tarefas.objects.filter(usuario=usuarioLogado)
        erros = request.GET.get('erro')
        return render(request, 'index.html', {'tarefas': tarefas, 'erro': erros})
    else:
        return redirect('/auth/login/?status=3')

def edicao_Tarefa(request):
    id_compromisso = request.POST.get('id_compromisso')
    nome_compromisso = request.POST.get('nome_compromisso')
    status_compromisso = request.POST.get('status_compromisso')
    data_compromisso = request.POST.get('data_compromisso')
    hora_inicio = request.POST.get('hora_inicio')
    hora_fim = request.POST.get('hora_fim')
    local_compromisso = request.POST.get('local_compromisso')
    observacoes = request.POST.get('observacoes')
    usuarioLogado = Usuario.objects.get(id=request.session['usuario'])
    tarefa = get_object_or_404(Tarefas, id=id_compromisso)

    return tarefa.check_conflito(request=request, data_compromisso=data_compromisso, hora_inicio=hora_inicio, hora_fim=hora_fim, usuarioLogado=usuarioLogado, nome_compromisso=nome_compromisso, status_compromisso=status_compromisso, local_compromisso=local_compromisso, observacoes=observacoes )

def add_Tarefa(request):
    nome_compromisso = request.POST.get('nome_compromisso')
    status_compromisso = request.POST.get('status_compromisso')
    data_compromisso = request.POST.get('data_compromisso')
    hora_inicio = request.POST.get('hora_inicio')
    hora_fim = request.POST.get('hora_fim')
    local_compromisso = request.POST.get('local_compromisso')
    observacoes = request.POST.get('observacoes')
    usuarioLogado = Usuario.objects.get(id=request.session['usuario'])

    tarefa = Tarefas(usuario=usuarioLogado)

    return tarefa.check_conflito(request=request, data_compromisso=data_compromisso, hora_inicio=hora_inicio, hora_fim=hora_fim, usuarioLogado=usuarioLogado, nome_compromisso=nome_compromisso, status_compromisso=status_compromisso, local_compromisso=local_compromisso, observacoes=observacoes )

def remove_Tarefa(request):
    id_compromisso = request.POST.get('id_compromisso')
    if request.session.get('usuario'):
        tarefas = Tarefas.objects.get(id=id_compromisso)
        if request.session.get('usuario') == tarefas.usuario.id:
            tarefa = Tarefas.objects.get(id=id_compromisso).delete()
            return redirect('/tarefa/index/')
        else:
            return redirect('/tarefa/index/?erro=1')
    else:
        return redirect('/auth/login/?status=2')



