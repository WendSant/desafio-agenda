from dataclasses import fields
from django import forms
from .models import Tarefas


class CadastroTarefa(forms.ModelForm):
    class Meta:
        model = Tarefas
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()
