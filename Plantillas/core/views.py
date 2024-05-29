
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from core.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from core.utils import generate_unique_username




#--------------- pagina principal-----------------------------

@login_required
def mostrar_html(request):
    return render(request, 'home.html', {
        'user': request.user,
    })





#--------------- Registrar cuenta-----------------------------

def register(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                new_user_name = generate_unique_username(request.POST.get('nombres'))
                user = User.objects.create_user(username=new_user_name,
                                                first_name=request.POST.get('nombres'),
                                                last_name=request.POST.get('apellidos'),
                                                email=request.POST.get('email'),
                                                password=request.POST.get('password1'))
                user.save()
                user = authenticate(request, username=new_user_name, password=request.POST.get('password1') )
                if user is not None:
                    login(request, user)
                    return redirect('inicio')
                else: return HttpResponse("La autenticación falló después de crear el usuario.")
            except IntegrityError:
                return render(request, 'signup.html', {'error': 'Este usuario ya existe.','enlace': 'login', 'options': 'Iniciar sesion'})
            except Exception as e:
                return HttpResponse('Error: {}'.format(str(e)))
        else: 
            return render(request, 'signup.html', {'enlace': 'login', 'options': 'Iniciar sesion', 'error': 'Las contraseñas no coinciden.'})
    
    else:
        return render(request, 'signup.html', {'enlace': 'login', 'options': 'Iniciar sesion'})





#--------------- Salir de la sesion-----------------------------
def Salir(request): #Go out
    logout(request)
    return redirect('login')
    





#--------------- inicio de sesion-----------------------------

def signin(request):

    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'GET':
        print("entro")
        return render(request, 'login.html', {
            'form': AuthenticationForm(),
            'options':'Crear cuenta',
            'enlace': 'registrar'})
         
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'login.html', {
            'form': AuthenticationForm(),
            'titulo': 'inicio de sesion',
            'options':'Crear cuenta',
            'botom': 'Inicio de sesion',
            'enlace': 'registrar',
            'error': 'El nombre o la contraseña del usuario son incorrectas'})
        else:
            login(request, user)
            return redirect('inicio')
        
        
        
        

def historial(request):
    user_name = request.user
    return render(request, 'Historial.html', {
        'user': request.user,
    })





@login_required
def edit_user(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user = request.user

        # Verificar contraseña actual
        if not user.check_password(current_password):
            messages.error(request, 'Contraseña actual incorrecta.')
            return redirect('editar')

        # Actualizar campos
        if 'image' in request.FILES:
            user.image = request.FILES['image']
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)

        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Mantener la sesión después de cambiar la contraseña

        user.save()
        messages.success(request, 'Usuario actualizado con éxito.')
        return redirect('editar')

    return render(request, 'editperfil.html', {'user': request.user,
                                               })