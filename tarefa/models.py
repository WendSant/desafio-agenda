import datetime

from django.db import models
from django.shortcuts import redirect

from usuarios.models import Usuario

status_choice = ('agendado', 'Agendado'), ('realizado', 'Realizado'), ('cancelado', 'Cancelado')


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

        if data_compromisso.strip() == '' or hora_inicio.strip()== '' or hora_fim.strip() =='' or nome_compromisso.strip() == '' or status_compromisso.strip()=='' or local_compromisso.strip() == '':
            return redirect('/tarefa/index/?erro=6')


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
        if data_compromisso < data_hoje:
            return redirect('/tarefa/index/?erro=4')  # Erro data já passou

        if not self.id:
            try:
                self = Tarefas(nome_compromisso=nome_compromisso, status_compromisso=status_compromisso,
                               data_compromisso=data_compromisso, hora_inicio=hora_inicio, hora_fim=hora_fim,
                               local_compromisso=local_compromisso, observacoes=observacoes, usuario=usuarioLogado)
                self.save()
                return redirect('/tarefa/index/')
            except:
                return redirect('/tarefa/index/?erro=1')

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
