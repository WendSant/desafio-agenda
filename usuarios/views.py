from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Usuario
from hashlib import sha256


def inicioRedirect(request):
    return redirect('/auth/login/')

def login(request):
    if request.session.get('usuario'):
        return redirect('/tarefa/index/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    usuario = Usuario.objects.filter(email = email)

    if len(nome.strip()) == 0 or len(email.strip()) ==0:
        return redirect('/auth/cadastro/?status=1') #Email e nome invalidos

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=4') #Senha precisa de 8+ caracteres

    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=2') #Email ja cadastrado

    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome= nome, senha= senha, email= email)
        usuario.save()
        return redirect('/auth/cadastro/?status=0') #Sucesso no cadastro
    except:
        return redirect('/auth/cadastro/?status=3') #Erro interno no sistema


def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)


    if len(Usuario.objects.filter(email = email)) > 0 and len(Usuario.objects.filter(senha = senha)) ==0:
        return redirect('/auth/login/?status=1') #Usuario cadastrado mas senha incorreta
    elif len(Usuario.objects.filter(email = email)) == 0:
        return redirect('/auth/login/?status=5') #Email não encontrado no sistema
    elif len(usuario) > 0:
        try: #Tentativa de login
            request.session['usuario'] = usuario[0].id #Pegando id usuario
            return redirect('/tarefa/index/')
        except:
            return redirect('/auth/login/?status=2')

def sair(request):
    try:
        request.session.flush()
        return redirect('/auth/login/?status=4') #Mensagem de deslogado com sucesso
    except:
        return redirect('/tarefa/index/?status=5') #Mensagem de erro no sistema