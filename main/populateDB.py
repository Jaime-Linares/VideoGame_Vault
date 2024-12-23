# encoding:utf-8
from main.models import Developer, Genre, Plataform, Store, Video_game
from bs4 import BeautifulSoup
import os, ssl, urllib.request, locale
from datetime import datetime
# lineas para evitar error SSL
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')



# --- FUNCIÓN PRINCIPAL PARA CARGAR LOS DATOS ------------------------------------------------------------------------------
def populate():
    # borramos todos los registros de la base de datos
    Developer.objects.all().delete()
    Genre.objects.all().delete()
    Plataform.objects.all().delete()
    Store.objects.all().delete()
    Video_game.objects.all().delete()

    NUM_PAGES = 3
    # cargamos los datos desde instant-gaming
    populate_instant_gaming(3)
    # cargamos los datos desde eneba
    populate_eneba(3)


# función auxiliar para tener los juegos en una lista y los generos de cada juego en un diccionario
def create_video_game(name, url_inf, url_img, price, discount, score, description, release_date, developer, generos, dic_genres, 
                      plataform, store, video_games_list):
    video_game = Video_game(name=name, url_inf=url_inf, url_img=url_img, price=price, discount=discount, score=score, description=description, 
                            release_date=release_date, developer=developer, plataform=plataform, store=store)
    video_games_list.append(video_game)
    dic_genres[url_inf] = generos
    return video_games_list, dic_genres


# función auxiliar para crear los videojuegos y los géneros y asociarlos unos a otros
def create_video_games(video_games_list, dic_genres, total_genres, store):
    total_genres = [ Genre(name=genre) for genre in total_genres ]
    Genre.objects.bulk_create(total_genres)
    print("GENRES CREATED")
    Video_game.objects.bulk_create(video_games_list)
    print("VIDEO GAMES CREATED")
    for video_game in Video_game.objects.all().filter(store=store):
        for genre in dic_genres[video_game.url_inf]:
            video_game.genres.add(Genre.objects.get(name=genre))



# --- FUNCIONES INSTANT-GAMING ---------------------------------------------------------------------------------------------
def populate_instant_gaming(num_pages):
    video_games_list = []
    dic_genres = {}
    total_genres = []
    dic_developers = {}
    dic_plataforms = {}
    store = Store.objects.create(name="Instant Gaming")
    print("START INSTANT GAMING WEB SCRAPPING")

    for pag in range(1, num_pages+1):
        request = urllib.request.Request(f"https://www.instant-gaming.com/es/busquedas/?page={pag}", headers={'User-Agent': 'Mozilla/5.0'})
        f = urllib.request.urlopen(request, timeout=3)
        s = BeautifulSoup(f, 'lxml')
        s_video_games = s.find("div", class_="listing-items").find_all("div", class_="force-badge")

        for s_video_game in s_video_games:
            name = str(list(s_video_game.find("div", class_="name").stripped_strings)[-1])
            url_inf = s_video_game.a['href'].strip()
            url_img = s_video_game.find("img", class_="picture")['data-src'].strip()

            request2 = urllib.request.Request(url_inf, headers={'User-Agent': 'Mozilla/5.0'})
            f2 = urllib.request.urlopen(request2)
            s2 = BeautifulSoup(f2, 'lxml')

            money = s2.find("div", class_="amount")
            price = float(money.find("div", class_="total").string.strip().replace("€", "").strip()) if money.find("div", class_="total") else 0.0
            discount = int(money.find("div", class_="discounted").string.strip().replace("%", "").replace("-", "").strip()) if money.find("div", class_="discounted") else 0
            s_score = s2.find("div", class_="ig-search-reviews-avg")
            if s_score != None and s_score.string.strip() != "--":
                score = float(s_score.string.strip())
            else:
                score = 0.0
            s_description = s2.find("div", class_="readable")
            description = "".join(list(s_description.stripped_strings)) if s_description else ""
            release_date = datetime.strptime(s2.find("div", class_="release-date").get_text().split(" -")[0].strip(), "%d %B %Y") if s2.find("div", class_="release-date") else None
            developer, dic_developers = get_developer_instant_gaming(s2, dic_developers)
            video_games_genres, total_genres = get_genres_instant_gaming(s2, total_genres)
            plataform, dic_plataforms = get_plataform_instant_gaming(s2, dic_plataforms)

            video_games_list, dic_genres = create_video_game(name, url_inf, url_img, price, discount, score, description, release_date, developer, 
                                                            video_games_genres, dic_genres, plataform, store, video_games_list)
    
    create_video_games(video_games_list, dic_genres, total_genres, store)
    print("FINISH INSTANT GAMING WEB SCRAPPING")


# función auxiliar para obtener el desarrollador de un videojuego
def get_developer_instant_gaming(s2, dic_developers):
    s_developer = s2.find("a", content="Developers")
    if s_developer:
        developer_string = s_developer.string.strip()
    else:
        developer_string = "Unknown"

    if developer_string not in dic_developers:
        developer = Developer.objects.create(name=developer_string)
        dic_developers[developer_string] = developer
    developer = dic_developers[developer_string]
    return developer, dic_developers


# función auxiliar para obtener los géneros de un videojuego
def get_genres_instant_gaming(s2, total_genres):
    video_games_genres = []

    s_genres = s2.find("div", class_="table-cell", string="Género:")
    if s_genres:
        s_genres = s_genres.next_sibling.next_sibling
        for a in s_genres.find_all("a"):
            genre = str(a.string.strip()).lower()
            video_games_genres.append(genre)
    s_features_genres = s2.find_all("span", class_="feature-text")
    if s_features_genres:
        for s_feature_genre in s_features_genres:
            if s_feature_genre.string.strip() not in video_games_genres:
                video_games_genres.append(s_feature_genre.string.strip().lower())

    for genre in video_games_genres:
        if genre not in total_genres:
            total_genres.append(genre)
    return video_games_genres, total_genres


# función auxiliar para obtener la plataforma de un videojuego
def get_plataform_instant_gaming(s2, dic_plataforms):
    s_plataform = s2.find("div", class_="subinfos").a
    if s_plataform:
        plataform_string = str(list(s_plataform.stripped_strings)[0]).lower()
    else:
        plataform_string = "Unknown"
    
    if plataform_string not in dic_plataforms:
        plataform = Plataform.objects.create(name=plataform_string)
        dic_plataforms[plataform_string] = plataform
    plataform = dic_plataforms[plataform_string]
    return plataform, dic_plataforms



# --- FUNCIONES ENEBA ------------------------------------------------------------------------------------------------------
def populate_eneba(num_pages):
    return None


