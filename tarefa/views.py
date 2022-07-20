from django.http import HttpResponse
from django.shortcuts import render, redirect
from usuarios.models import Usuario


def index(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario']).nome
        return HttpResponse(f'olá {usuario}')
    else:
        return redirect('/auth/login/?status=3')