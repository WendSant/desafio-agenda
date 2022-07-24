from django.db import models
from usuarios.models import Usuario

status_choice = ('agendado', 'Agendado'),('realizado', 'Realizado'), ('cancelado', 'Cancelado')

class Tarefas(models.Model):
    status_compromisso = models.CharField(max_length= 200, choices= status_choice)
    nome_compromisso = models.CharField(max_length=100)
    data_compromisso = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    local_compromisso = models.CharField(max_length=50)
    observacoes = models.CharField(max_length = 250, blank= True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome_compromisso
    
    class Meta:
        verbose_name = 'Tarefa'

