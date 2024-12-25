from django.shortcuts import render, get_object_or_404
from main.models import Developer, Genre, Plataform, Store, Video_game
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from main.populateDB import populate
from main.forms import GenreSelectionForm



# vista para mostrar la página de inicio
def home(request):
    developers = Developer.objects.all().count()
    genres = Genre.objects.all().count()
    plataforms = Plataform.objects.all().count()
    stores = Store.objects.all().count()
    video_games = Video_game.objects.all().count()
    return render(request, 'home.html', {'developers':developers, 'genres':genres, 'plataforms':plataforms, 'stores':stores, 'video_games':video_games})


# vista para loguearse
def sign_in(request):
    formulario = AuthenticationForm()

    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        acceso = authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/'))
            else:
                return render(request, 'error.html', {'error':"USUARIO NO ACTIVO"})
        else:
            return render(request, 'error.html', {'error':"USUARIO O CONTRASEÑA INCORRECTOS"})
                     
    return render(request, 'login.html', {'formulario':formulario})


# vista para desloguearse
@login_required(login_url='/login/')
def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')


# vista para registrarse
def sign_up(request):
    formulario = UserCreationForm()

    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                usuario = request.POST['username']
                clave = request.POST['password1']
                acceso = authenticate(username=usuario, password=clave)
                if acceso is not None:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
            except ValueError as e:
                formulario.add_error(None, str(e))

    return render(request, 'register.html', {'formulario': formulario})


# vista para cargar los datos
@login_required(login_url='/login/')
def load_data(request):
    populate()
    return HttpResponseRedirect('/')


# vista para mostrar todos los videojuegos
def show_all_video_games(request):
    video_games = Video_game.objects.all()
    return render(request, 'all_video_games.html', {'video_games':video_games})


# vista para mostrar los detalles de un videojuego y sus videojuegos recomendados según su parecido
# utilizando el SR basado en contenido
def show_video_game(request, video_game_id):
    video_game = get_object_or_404(Video_game, pk=video_game_id)
    video_games_recommended = Video_game.objects.all()[:4]  # cambiar por el SR basado en contenido
    return render(request, 'video_game.html', {'video_game':video_game, 'video_games_recommended':video_games_recommended})


# vista para mostrar los videojuegos que son de un género específico
def show_video_games_selected_genre(request):
    formulario = GenreSelectionForm()
    video_games = None
    genre = None
    
    if request.method=='POST':
        formulario = GenreSelectionForm(request.POST)
        if formulario.is_valid():
            genre = formulario.cleaned_data['genre']
            video_games = genre.video_game_set.all()
            
    return render(request, 'video_games_selected_genre.html', {'formulario':formulario, 'video_games':video_games, 'genre':genre})

