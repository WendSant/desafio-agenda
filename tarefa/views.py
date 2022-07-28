import csv
import datetime

from django.http import HttpResponse
from django.utils.timezone import now, localtime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from usuarios.models import Usuario
from .models import Tarefas


def index(request):
    if request.session.get('usuario'):
        usuarioLogado = Usuario.objects.get(id=request.session['usuario'])
        erros = request.GET.get('erro')
        tarefas = Tarefas.objects.filter(usuario=usuarioLogado)
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

    return tarefa.check_conflito(request=request, data_compromisso=data_compromisso, hora_inicio=hora_inicio,
                                 hora_fim=hora_fim, usuarioLogado=usuarioLogado, nome_compromisso=nome_compromisso,
                                 status_compromisso=status_compromisso, local_compromisso=local_compromisso,
                                 observacoes=observacoes)


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

    return tarefa.check_conflito(request=request, data_compromisso=data_compromisso, hora_inicio=hora_inicio,
                                 hora_fim=hora_fim, usuarioLogado=usuarioLogado, nome_compromisso=nome_compromisso,
                                 status_compromisso=status_compromisso, local_compromisso=local_compromisso,
                                 observacoes=observacoes)


def remove_Tarefa(request):
    id_compromisso = request.POST.get('id_compromisso')
    if request.session.get('usuario'):
        tarefas = Tarefas.objects.get(id=id_compromisso)
        if request.session.get('usuario') == tarefas.usuario.id:
            tarefa = Tarefas.objects.get(id=id_compromisso).delete()
            return redirect('/tarefa/index/')
        else:
            return redirect('/tarefa/index/?erro=1')  # Erro interno no sistema
    else:
        return redirect('/auth/login/?status=2')


def filtrar_Tarefa(request):
    tarefa = Tarefas()
    return tarefa.filtrar(request=request)


def exportar_planilha(request):
    global response
    if request.method == 'POST':
        usuarioLogado = Usuario.objects.get(id=request.session['usuario'])
        tarefas = Tarefas.objects.filter(usuario=usuarioLogado)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=ConsultaTarefas' + str(datetime.datetime.now()) + '.csv'
        writer = csv.writer(response)
        writer.writerow(['Status_Compromisso', 'Nome_Compromisso', 'Data_Compromisso', 'Hora_Inicio', 'Hora_Fim', 'Local_Compromisso', 'Observações'])

        for info in tarefas:
            if ',' in info.local_compromisso:
               info.local_compromisso= info.local_compromisso.replace(',', ' ')
            if ',' in info.observacoes:
                info.observacoes = info.observacoes.replace(',', ' ')
            writer.writerow(
                [info.status_compromisso, info.nome_compromisso, info.data_compromisso, info.hora_fim, info.hora_fim, info.local_compromisso, info.observacoes])
    return response
