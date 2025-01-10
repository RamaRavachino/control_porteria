from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('pagina_principal')  # Redirige a la página principal tras el login
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'autenticacion/login.html')  # Renderiza el formulario de login
