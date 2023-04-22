from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import FormContato


def login(request):
    if request.method != "POST":
        return render(request, 'accounts/login.html')

    user = request.POST.get("user")
    password = request.POST.get("password")

    user = auth.authenticate(request, username=user, password=password)

    if not user:
        messages.error(request, "Usuario ou senha inválidos.")
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, "Você logou com sucesso.")
        return redirect("dashboard")


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != "POST":
        return render(request, 'accounts/register.html')

    name = request.POST.get("name")
    user = request.POST.get("user")
    email = request.POST.get("email")
    password = request.POST.get("password")
    password2 = request.POST.get("password2")

    if not name or not user or not email or not password or not password2:
        messages.error(request, "Nenhum campo pode ficar em branco.")
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, "Email invalido!")
        return render(request, 'accounts/register.html')

    if len(password) < 6:
        messages.error(request, "Senha precisa conter 6 ou mais caracteres.")
        return render(request, 'accounts/register.html')

    if len(user) < 3:
        messages.error(request, "Usuario precisa conter mais de 3 letras")
        return render(request, 'accounts/register.html')

    if password != password2:
        messages.error(request, "As senhas precisam ser iguais.")
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=user).exists():
        messages.error(request, "Usuario ja existente")
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email ja existente.")
        return render(request, 'accounts/register.html')

    messages.success(request, "Usuario registrado com sucesso, faça login.")

    usuario = User.objects.create_user(username=user, email=email,
                                       password=password, first_name=name
                                       )
    usuario.save()
    return redirect("login")


@login_required(redirect_field_name="login")
def dashboard(request):
    if request.method != "POST":
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, "Erro ao enviar formulário.")
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(
        request, f'Contato {request.POST.get("nome")} salvo com sucesso')
    return redirect('dashboard')
