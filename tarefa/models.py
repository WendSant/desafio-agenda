from django.db import models


status_choice = ('agendado', 'Agendado'),('realizado', 'Realizado'), ('cancelado', 'Cancelado')

class Tarefas(models.Model):
    status_compromisso = models.CharField(max_length= 200, choices= status_choice)
    nome_compromisso = models.CharField(max_length=200)
    data_compromisso = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models. TimeField()
    local_compromisso = models.CharField(max_length=50)
    observacoes = models.CharField(max_length = 250, blank= True)
    
    class Meta:
        verbose_name = 'Tarefa'

    def __srt__(self):
        return self.nome_compromisso