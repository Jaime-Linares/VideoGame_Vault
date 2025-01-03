from django.shortcuts import render, get_object_or_404
from main.models import Developer, Genre, Plataform, Store, Video_game
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from main.populateDB import populate
from main.forms import GenreSelectionForm, DeveloperSelectionForm, PlataformSelectionForm, StoreSelectionForm, DateRangeForm, MaxPriceForm, SearchNameOrDescriptionForm, GenreAndSearchNameForm
from main.whoosh import video_games_in_period, video_games_selected_max_price, video_games_with_words, video_games_by_genre_and_words, video_games_by_description
from main.recommendations import generate_and_save_recommendations, get_recommendations_for_game


# dirección para almacenar el índice de whoosh
DIR_WHOOSH_INDEX = "Index"
# dirección para almacenar las recomendaciones
DIR_RS_DATA = "dataRS.dat"
# recomendaciones basadas en contenido
recommendations = None



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
    populate(DIR_WHOOSH_INDEX)
    return HttpResponseRedirect('/')


# vista para generar y guardar las recomendaciones
@login_required(login_url='/login/')
def load_recommendations_system(request):
    generate_and_save_recommendations(DIR_RS_DATA)
    return HttpResponseRedirect('/')


# vista para mostrar todos los videojuegos
def show_all_video_games(request):
    video_games = Video_game.objects.all()
    return render(request, 'all_video_games.html', {'video_games':video_games})


# vista para mostrar los detalles de un videojuego y sus videojuegos recomendados según su parecido
# utilizando el SR basado en contenido
def show_video_game(request, video_game_id):
    global recommendations
    video_games_recommended = []
    video_game = get_object_or_404(Video_game, pk=video_game_id)
    # obtener las recomendaciones para el videojuego
    recommended_ids = get_recommendations_for_game(video_game_id, DIR_RS_DATA, recommendations)
    if recommended_ids:
        video_games_recommended = Video_game.objects.filter(id__in=recommended_ids)

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


# vista para mostrar los videojuegos que son de un desarrollador específico
def show_video_games_selected_developer(request):
    formulario = DeveloperSelectionForm()
    video_games = None
    developer = None
    
    if request.method=='POST':
        formulario = DeveloperSelectionForm(request.POST)
        if formulario.is_valid():
            developer = formulario.cleaned_data['developer']
            video_games = Video_game.objects.filter(developer=developer)
            
    return render(request, 'video_games_selected_developer.html', {'formulario':formulario, 'video_games':video_games, 'developer':developer})


# vista para mostrar los videojuegos que son de una plataforma específica
def show_video_games_selected_plataform(request):
    formulario = PlataformSelectionForm()
    video_games = None
    plataform = None
    
    if request.method=='POST':
        formulario = PlataformSelectionForm(request.POST)
        if formulario.is_valid():
            plataform = formulario.cleaned_data['plataform']
            video_games = Video_game.objects.filter(plataform=plataform)
            
    return render(request, 'video_games_selected_plataform.html', {'formulario':formulario, 'video_games':video_games, 'plataform':plataform})


# vista para mostrar los videojuegos que son de una tienda específica
def show_video_games_selected_store(request):
    formulario = StoreSelectionForm()
    video_games = None
    store = None
    
    if request.method=='POST':
        formulario = StoreSelectionForm(request.POST)
        if formulario.is_valid():
            store = formulario.cleaned_data['store']
            video_games = Video_game.objects.filter(store=store).select_related('developer', 'store')
            
    return render(request, 'video_games_selected_store.html', {'formulario':formulario, 'video_games':video_games, 'store':store})


# vista para mostrar los videojuegos cuya fecha de lanzamiento se encuentre en el rango especificado utilizando whoosh
@login_required(login_url='/login/')
def show_video_games_in_period(request):
    formulario = DateRangeForm()
    grouped = None
    video_games = None
    video_games_by_genre = {}
    start_date = None
    end_date = None

    if request.method == 'POST':
        formulario = DateRangeForm(request.POST)
        if formulario.is_valid():
            start_date = formulario.cleaned_data['start_date']
            end_date = formulario.cleaned_data['end_date']
            grouped = formulario.cleaned_data['grouped']
            video_games = video_games_in_period(DIR_WHOOSH_INDEX, start_date, end_date)

            if grouped:
                for video_game in video_games:
                    genres = video_game.genres.all()
                    for genre in genres:
                        if genre in video_games_by_genre:
                            video_games_by_genre[genre].append(video_game)
                        else:
                            video_games_by_genre[genre] = [video_game]

    return render(request, 'video_games_in_period.html', {'formulario': formulario, 'video_games_by_genre': video_games_by_genre, 'video_games': video_games,
                                                          'start_date': start_date, 'end_date': end_date, 'grouped': grouped})  


# vista para mostrar los videojuegos que tienen un precio menor o igual al especificado utilizando whoosh
@login_required(login_url='/login/')
def show_video_games_selected_max_price(request):
    formulario = MaxPriceForm()
    video_games = None
    max_price = None

    if request.method == 'POST':
        formulario = MaxPriceForm(request.POST)
        if formulario.is_valid():
            max_price = formulario.cleaned_data['max_price']
            video_games = video_games_selected_max_price(DIR_WHOOSH_INDEX, max_price)

    return render(request, 'video_games_max_price.html', {'formulario': formulario, 'video_games': video_games, 'max_price': max_price})  


# vista para mostrar los videojuegos más relevantes que contienen la/s palabra/s especificada/s en el título o descripción utilizando whoosh
@login_required(login_url='/login/')
def show_relevant_video_games_with_words_in_title_or_description(request):
    formulario = SearchNameOrDescriptionForm()
    video_games = None
    words = None

    if request.method == 'POST':
        formulario = SearchNameOrDescriptionForm(request.POST)
        if formulario.is_valid():
            words = formulario.cleaned_data['words']
            video_games = video_games_with_words(DIR_WHOOSH_INDEX, words)

    return render(request, 'video_games_with_words_in_title_or_description.html', {'formulario': formulario, 'video_games': video_games, 'words': words})


# vista para mostrar los videojuegos más relevantes que son de un género específico y que contienen la/s palabra/s especificada/s en el título utilizando whoosh
@login_required(login_url='/login/')
def show_relevant_video_games_selected_genre_and_words_in_title(request):
    formulario = GenreAndSearchNameForm()
    video_games = None
    genre = None
    words = None

    if request.method == 'POST':
        formulario = GenreAndSearchNameForm(request.POST)
        if formulario.is_valid():
            genre = formulario.cleaned_data['genre']
            words = formulario.cleaned_data['words']
            video_games = video_games_by_genre_and_words(DIR_WHOOSH_INDEX, genre, words)

    return render(request, 'video_games_selected_genre_and_words_in_title.html', {'formulario': formulario, 'video_games': video_games, 'genre': genre, 
                                                                                  'words': words})


# vista para mostrar los videojuegos más relevantes que contienen la frase especificada en la descripción utilizando whoosh
@login_required(login_url='/login/')
def show_relevant_video_games_with_sentence_in_description(request):
    formulario = SearchNameOrDescriptionForm()
    video_games = None
    sentence = None

    if request.method == 'POST':
        formulario = SearchNameOrDescriptionForm(request.POST)
        if formulario.is_valid():
            sentence = formulario.cleaned_data['words']
            video_games = video_games_by_description(DIR_WHOOSH_INDEX, sentence)

    return render(request, 'video_games_with_sentence_in_description.html', {'formulario': formulario, 'video_games': video_games, 'sentence': sentence})

