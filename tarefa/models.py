import datetime

from django.db import models
from django.shortcuts import redirect, render

from usuarios.models import Usuario

status_choice = ('agendado', 'agendado'), ('realizado', 'realizado'), ('cancelado', 'cancelado')


class Tarefas(models.Model):
    status_compromisso = models.CharField(max_length=200, choices=status_choice)
    nome_compromisso = models.CharField(max_length=100)
    data_compromisso = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    local_compromisso = models.CharField(max_length=50)
    observacoes = models.CharField(max_length=250, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome_compromisso

    class Meta:
        verbose_name = 'Tarefa'

    def check_conflito(self, request, data_compromisso, hora_inicio, hora_fim, usuarioLogado, nome_compromisso,
                       status_compromisso, local_compromisso, observacoes):

        if data_compromisso.strip() == '' or hora_inicio.strip() == '' or hora_fim.strip() == '' or nome_compromisso.strip() == '' or status_compromisso.strip() == '' or local_compromisso.strip() == '':
            return redirect('/tarefa/index/?erro=6')  # Preencha todos os campos

        hora_inicialVerify = datetime.datetime.strptime(hora_inicio, '%H:%M')
        hora_finalVerify = datetime.datetime.strptime(hora_fim, '%H:%M')
        if hora_inicialVerify > hora_finalVerify:
            return redirect('/tarefa/index/?erro=5')  # Erro hora inicial maior que hora final

        if self.usuario.id != request.session['usuario']:
            return redirect('/tarefa/index/?erro=2')  # Erro tarefa invalida caso usuario tente mudar o id

        # Filtrando uma gambiarra
        tarefas = Tarefas.objects.filter(usuario=usuarioLogado, data_compromisso=data_compromisso,
                                         hora_inicio__range=[hora_inicio, hora_fim])
        tarefas2 = Tarefas.objects.filter(usuario=usuarioLogado, data_compromisso=data_compromisso,
                                          hora_fim__range=[hora_inicio, hora_fim])

        for contador in range(tarefas.count()):
            if tarefas[contador].id == self.id:
                pass
            else:
                return redirect('/tarefa/index/?erro=3')  # Erro conflito de hora
        for contador in range(tarefas2.count()):
            if tarefas2[contador].id == self.id:
                pass
            else:
                return redirect('/tarefa/index/?erro=3')  # Erro conflito de hora

        data_hoje = datetime.date.today()
        data_hoje = data_hoje.__str__()

        if not self.id:
            try:
                if data_compromisso < data_hoje:
                    return redirect('/tarefa/index/?erro=4')  # Erro data já passou
                self = Tarefas(nome_compromisso=nome_compromisso, status_compromisso=status_compromisso,
                               data_compromisso=data_compromisso, hora_inicio=hora_inicio, hora_fim=hora_fim,
                               local_compromisso=local_compromisso, observacoes=observacoes, usuario=usuarioLogado)
                self.save()
                return redirect('/tarefa/index/')
            except:
                return redirect('/tarefa/index/?erro=1')  # Erro interno no sistema

        try:
            self.nome_compromisso = nome_compromisso
            self.status_compromisso = status_compromisso
            self.data_compromisso = data_compromisso
            self.hora_inicio = hora_inicio
            self.hora_fim = hora_fim
            self.local_compromisso = local_compromisso
            self.observacoes = observacoes
            self.save()
            return redirect('/tarefa/index/')
        except:
            return redirect('/tarefa/index/?erro=1')  # Erro interno no sistema

    def filtrar(self, request):
        usuarioLogado = Usuario.objects.get(id=request.session['usuario'])
        erros = request.GET.get('erro')
        nome_compromisso = request.POST.get('nome_compromisso')
        status_compromisso = request.POST.get('status_compromisso')
        data_compromisso = request.POST.get('data_compromisso')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')
        local_compromisso = request.POST.get('local_compromisso')
        observacoes = request.POST.get('observacoes')

        # print(nome_compromisso)
        # print(status_compromisso)
        # print(data_compromisso)
        # print(local_compromisso)
        # print(f'HORA INICIO{hora_inicio}')
        # print(f'HORA fim{hora_fim}')

        if observacoes.strip() == '':
            observacoes = None

        if nome_compromisso or data_compromisso or local_compromisso or status_compromisso or hora_inicio or hora_fim or observacoes:
            if (hora_fim or hora_inicio) and not data_compromisso:
                return redirect('/tarefa/index/?erro=7')  # Erro preencha uma data para consultar horas
            try:
                if (hora_inicio and hora_fim) and data_compromisso:
                    tarefa = Tarefas.objects.filter(usuario=usuarioLogado, data_compromisso=data_compromisso, hora_inicio__range=[hora_inicio,hora_fim]) or Tarefas.objects.filter(usuario=usuarioLogado, data_compromisso=data_compromisso, hora_fim__range=[hora_inicio,hora_fim])
                    return render(request, 'index.html', {'tarefas': tarefa, 'erro': erros})
                elif observacoes and not status_compromisso and not local_compromisso and not data_compromisso and not nome_compromisso and not hora_fim and not hora_inicio:
                    try:
                        obs = Tarefas.objects.filter(usuario=usuarioLogado, observacoes=observacoes)
                        tarefa = obs
                        return render(request, 'index.html', {'tarefas': tarefa, 'erro': erros})
                    except:
                        return redirect('/tarefa/index/?erro=8')
                else:
                    tarefa = Tarefas.objects.filter(usuario=usuarioLogado,
                                                     nome_compromisso=nome_compromisso) or Tarefas.objects.filter(
                        usuario=usuarioLogado, status_compromisso=status_compromisso) or Tarefas.objects.filter(
                        usuario=usuarioLogado, local_compromisso=local_compromisso) or Tarefas.objects.filter(
                        usuario=usuarioLogado, data_compromisso=data_compromisso) or Tarefas.objects.filter(
                        usuario=usuarioLogado, hora_inicio__range=[hora_inicio, hora_fim]) or Tarefas.objects.filter(
                        usuario=usuarioLogado,
                        hora_fim__range=[hora_inicio, hora_fim])
                    if tarefa.count() == 0:
                        return redirect('/tarefa/index/?erro=8')
                    return render(request, 'index.html', {'tarefas': tarefa, 'erro': erros})
            except:
                return redirect('/tarefa/index/?erro=8')  # Nenhuma tarefa encontrada
        return redirect('/tarefa/index/')
