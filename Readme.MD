# Desafio para Desenvolvedor Web Python JR
[![Python Version](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-4.0.6-blue.svg)](https://djangoproject.com)


<div align="center">

### O objetivo do desafio é desenvolver uma agenda de compromissos, onde o usuário poderá cadastrar suas tarefas diárias.

<br>
<p>
    Imagem tela login:
</p>
<img src="https://user-images.githubusercontent.com/79418546/181603111-e10528d1-e26d-4364-97db-af2ae5375df7.png" width="1000px">
<img>
<p>
    Imagem painel de tarefas:
</p>
<img src="https://user-images.githubusercontent.com/79418546/181601477-8f743235-b86a-4ac6-9e1e-1acd2864b2a6.png" width="1000px">
<img>
<p>
    Imagem adicionando tarefa:
</p>
<img src="https://user-images.githubusercontent.com/79418546/181602788-72c5d16c-10ad-4d2c-af1f-3b4a49f9c076.png" width="1000px">
<img>

</div>

<div align="center">

### Para quem deseja rodar a aplicação em sua maquina uma breve explicação sobre como subir ela. A aplicação foi feita em ambiente Windows 10(utilizando bash)

</div>
<br>

- <p style="font-size: 15px;" >Primeiramente tenha uma versão do python igual ou  acima da versão 3.8 instalado no seu ambiente</p>
- <p style="font-size: 15px;" > Se não tiver o pip instalado faça a instalação </>

- <p style="font-size: 15px;" > No diretorio do projeto e com pip instalado comece a instalar o virtualenv </>
```
$ pip install virtualenv
```
- <p style="font-size: 15px;" > Utilize um dos seguintes comandos para gerar a venv: </>
```
$ virtualenv venv ou python -m venv venv
```
- <p style="font-size: 15px;" > Após isso é hora de iniciar o ambiente virtual</>
```
$ source venv/Scripts/activate 
```
- <p style="font-size: 15px;" > Agora rode esse comando para instalar todos os requirements</>
```
$ pip install -r requirements.txt 
```
- <p style="font-size: 15px;" > Antes de iniciar a aplicação rode o makemigrations: </>
```
$ python manage.py makemigrations
```
- <p style="font-size: 15px;" > E logo após rode o migrate: </>
```
$ python manage.py migrate
```
- <p style="font-size: 15px;" > A aplicação esta pronta para funcionar, agora basta você iniciá-la com esse comando: </>
```
$ python manage.py runserver 
```
- <p style="font-size: 15px;" >Deve ser lembrado que alguns comandos podem mudar de acordo com as versões instaladas em seu ambiente</>

<div align="center">

<p>
<!-- Image Shields -->
<img  alt="Languages Count"  src="https://img.shields.io/github/languages/count/WendSant/desafio-agenda">
<img  alt="Last Commit"  src="https://img.shields.io/github/last-commit/WendSant/desafio-agenda">
<img  alt="Repo Size"  src="https://img.shields.io/github/repo-size/WendSant/desafio-agenda">
</p>
</div>