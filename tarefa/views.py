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

    hora_inicialVerify = datetime.datetime.strptime(hora_inicio, '%H:%M')
    hora_finalVerify = datetime.datetime.strptime(hora_fim, '%H:%M')
    if hora_inicialVerify > hora_finalVerify:
        return redirect('/tarefa/index/?erro=5')

    if tarefa.usuario.id != request.session['usuario']:
        return redirect('/tarefa/index/?erro=2') #Erro tarefa invalida caso usuario tente mudar o id

    # Filtrando uma gambiarra
    tarefas = Tarefas.objects.filter(usuario=usuarioLogado, data_compromisso=data_compromisso,
                                     hora_inicio__range=[hora_inicio, hora_fim])
    tarefas2 = Tarefas.objects.filter(usuario=usuarioLogado, data_compromisso=data_compromisso,
                                      hora_fim__range=[hora_inicio, hora_fim])

    # print(tarefas.filter(nome_compromisso= nome_compromisso, status_compromisso=status_compromisso, data_compromisso=data_compromisso, hora_inicio= hora_inicio, hora_fim= hora_fim,local_compromisso=local_compromisso, observacoes= observacoes))

    for contador in range(tarefas.count()):
        if tarefas[contador].id == tarefa.id:
            pass
        else:
            return redirect('/tarefa/index/?erro=3') #Erro conflito de hora
    for contador in range(tarefas2.count()):
        if tarefas2[contador].id == tarefa.id:
            pass
        else:
            return redirect('/tarefa/index/?erro=3') #Erro conflito de hora

    data_hoje = datetime.date.today()
    data_hoje = data_hoje.__str__()
    if data_compromisso < data_hoje:
        return redirect('/tarefa/index/?erro=4') #Erro data já passou

    try:
        tarefa.nome_compromisso = nome_compromisso
        tarefa.status_compromisso = status_compromisso
        tarefa.data_compromisso = data_compromisso
        tarefa.hora_inicio = hora_inicio
        tarefa.hora_fim = hora_fim
        tarefa.local_compromisso = local_compromisso
        tarefa.observacoes = observacoes
        tarefa.save()
        return redirect('/tarefa/index/')
    except:
        return redirect('/tarefa/index/?erro=1') #Erro interno no sistema
