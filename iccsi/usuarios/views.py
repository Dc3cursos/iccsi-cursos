from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroAlumnoForm, RegistroProfesorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Usuario

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
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Por favor ingresa tu correo electrónico y contraseña.')
            return render(request, 'usuarios/login.html')
        
        # Buscar usuario por email
        try:
            user = Usuario.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except Usuario.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            # Redirigir según el rol de usuario
            if hasattr(user, 'rol'):
                if user.rol == 'profesor':
                    return redirect('panel_profesor')
                else:
                    return redirect('panel_usuario')
            else:
                return redirect('panel_usuario')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'usuarios/home.html')

@login_required
def panel_usuario(request):
    usuario = request.user
    return render(request, 'usuarios/panel_usuario.html', {'usuario': usuario})

@login_required
def panel_profesor(request):
    usuario = request.user
    # Verificar que el usuario sea profesor
    if not hasattr(usuario, 'rol') or usuario.rol != 'profesor':
        messages.error(request, 'Acceso denegado. Solo los profesores pueden acceder a este panel.')
        return redirect('panel_usuario')
    
    # Obtener los cursos del profesor
    from iccsi.cursos.models import Curso
    cursos_profesor = Curso.objects.filter(profesor=usuario)
    
    context = {
        'usuario': usuario,
        'cursos': cursos_profesor,
        'total_cursos': cursos_profesor.count(),
    }
    return render(request, 'usuarios/panel_profesor.html', context)

def terminos(request):
    """Términos y Condiciones de Uso"""
    return render(request, 'usuarios/terminos.html')

def privacidad(request):
    """Política de Privacidad"""
    return render(request, 'usuarios/privacidad.html')

def cookies(request):
    """Política de Cookies"""
    return render(request, 'usuarios/cookies.html')

def aviso_legal(request):
    """Aviso Legal"""
    return render(request, 'usuarios/aviso_legal.html')

from .models import DenunciaFalsificacion

def reportar_falsificacion(request):
    """Página para reportar falsificaciones de certificados DC-3"""
    if request.method == 'POST':
        try:
            # Crear la denuncia
            denuncia = DenunciaFalsificacion.objects.create(
                nombre_denunciante=request.POST.get('nombre_denunciante'),
                email_denunciante=request.POST.get('email_denunciante'),
                telefono=request.POST.get('telefono', ''),
                denuncia_anonima=request.POST.get('denuncia_anonima') == 'on',
                tipo_denuncia=request.POST.get('tipo_denuncia'),
                descripcion=request.POST.get('descripcion'),
                folio_certificado=request.POST.get('folio_certificado', ''),
                codigo_verificacion=request.POST.get('codigo_verificacion', ''),
                ubicacion=request.POST.get('ubicacion', ''),
                fecha_incidente=request.POST.get('fecha_incidente') or None,
                procesado_por=request.user if request.user.is_authenticated else None
            )
            
            # Procesar evidencia si se subió
            if 'evidencia' in request.FILES:
                denuncia.evidencia = request.FILES['evidencia']
                denuncia.save()
            
            messages.success(request, f'Denuncia #{denuncia.id} recibida exitosamente. Nuestro equipo legal la revisará en las próximas 24 horas.')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, 'Error al procesar la denuncia. Por favor, intenta nuevamente.')
            return redirect('reportar_falsificacion')
    
    return render(request, 'usuarios/reportar_falsificacion.html')