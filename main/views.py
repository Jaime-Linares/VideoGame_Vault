from django.shortcuts import render
from main.models import Developer, Genre, Plataform, Store, Video_game



# vista para mostrar la página de inicio
def home(request):
    developers = Developer.objects.all().count()
    genres = Genre.objects.all().count()
    plataforms = Plataform.objects.all().count()
    stores = Store.objects.all().count()
    video_games = Video_game.objects.all().count()
    return render(request, 'home.html', {'developers':developers, 'genres':genres, 'plataforms':plataforms, 'stores':stores, 'video_games':video_games})

