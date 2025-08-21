from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroAlumnoForm, RegistroProfesorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def registro_alumno(request):
    if request.method == 'POST':
        form = RegistroAlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de alumno exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroAlumnoForm()
    return render(request, 'usuarios/registro_alumno.html', {'form': form})

def registro_profesor(request):
    if request.method == 'POST':
        form = RegistroProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de profesor exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroProfesorForm()
    return render(request, 'usuarios/registro_profesor.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel_usuario')  # <--- Redirige al panel de usuario
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
    from django.shortcuts import render

def home(request):
    return render(request, 'usuarios/home.html')
    from django.contrib.auth.decorators import login_required

@login_required
def panel_usuario(request):
    usuario = request.user
    return render(request, 'usuarios/panel_usuario.html', {'usuario': usuario})