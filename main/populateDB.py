# encoding:utf-8
from main.models import Developer, Genre, Plataform, Store, Video_game
from bs4 import BeautifulSoup
import os, ssl, urllib.request, locale, time, shutil
from datetime import datetime
from urllib.error import HTTPError
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD, ID, NUMERIC
# lineas para evitar error SSL
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


# --- VARIABLES GLOBALES ---------------------------------------------------------------------------------------------------
# para establecer el idioma de las fechas
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# para traducir ciertos géneros
genre_traductor = {"aventuras":"aventura","cooperativo online":"cooperativo en línea","indie":"indies","un solo jugador":"un jugador", 
                   "fps":"fps / tps", "pr√©stamo familiar":"préstamo familiar", "cooperativo en l√≠nea":"cooperativo en línea"}



# --- FUNCIÓN PRINCIPAL PARA CARGAR LOS DATOS ------------------------------------------------------------------------------
def populate(dir_index):
    # borramos todos los registros de la base de datos
    Developer.objects.all().delete()
    Genre.objects.all().delete()
    Plataform.objects.all().delete()
    Store.objects.all().delete()
    Video_game.objects.all().delete()

    # creamos el esquema de whoosh, eliminamos el directorio del índice si existe y creamos el índice
    schema = Schema(name=TEXT(stored=True, phrase=True), url_inf=ID(stored=True, unique=True), price=NUMERIC(stored=True, numtype=float),
                    discount=NUMERIC(stored=True, numtype=int), score=NUMERIC(stored=True, numtype=float), description=TEXT(stored=True, phrase=True),
                    release_date=DATETIME(stored=True), developer=TEXT(stored=True, phrase=True), genres=KEYWORD(stored=True, commas=True, lowercase=True),
                    plataform=TEXT(stored=True, phrase=True), store=TEXT(stored=True, phrase=True))
    
    if os.path.exists(dir_index):
        shutil.rmtree(dir_index)
    os.mkdir(dir_index)

    ix = create_in(dir_index, schema=schema)

    # variables importantes
    NUM_PAGES_INSTANT_GAMING = 5    # puedes usarse el valor que quiera, pero entre más alto, más tiempo tardará
    NUM_PAGES_ENEBA = 1    # se recomienda no poner más de 1 o 2 porque eneba bloquea las peticiones (error 429 -> too many requests)
    dic_developers = {}
    total_genres = []
    dic_genres = {}
    dic_plataforms = {}

    # cargamos los datos desde instant-gaming
    populate_instant_gaming(dir_index, NUM_PAGES_INSTANT_GAMING, dic_developers, total_genres, dic_genres, dic_plataforms)
    # cargamos los datos desde eneba
    populate_eneba(dir_index, NUM_PAGES_ENEBA, dic_developers, total_genres, dic_genres, dic_plataforms)
    print("FINISH POPULATE DATABASE AND WHOOSH INDEX")


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
def populate_instant_gaming(dir_index, num_pages, dic_developers, total_genres, dic_genres, dic_plataforms):
    video_games_list = []
    store = Store.objects.create(name="Instant Gaming")
    print("START INSTANT GAMING WEB SCRAPPING")

    ix = open_dir(dir_index)
    writer = ix.writer()

    for page in range(1, num_pages+1):
        request = urllib.request.Request(f"https://www.instant-gaming.com/es/busquedas/?page={page}", headers={'User-Agent': 'Mozilla/5.0'})
        f = urllib.request.urlopen(request, timeout=3)
        s = BeautifulSoup(f, 'lxml')
        s_video_games = s.find("div", class_="listing-items").find_all("div", class_="force-badge")

        for s_video_game in s_video_games:
            is_dlc = s_video_game.find("span", class_="dlc")
            if is_dlc and is_dlc.string.strip() == "DLC":   # si es un DLC no lo añadimos porque no es un videojuego sino un contenido descargable
                continue
            name = str(list(s_video_game.find("div", class_="name").stripped_strings)[-1])
            url_inf = s_video_game.a['href'].strip()
            url_img = s_video_game.find("img", class_="picture")['data-src'].strip()

            request2 = urllib.request.Request(url_inf, headers={'User-Agent': 'Mozilla/5.0'})
            f2 = urllib.request.urlopen(request2)
            s2 = BeautifulSoup(f2, 'lxml')

            money = s2.find("div", class_="amount")
            price_str = money.find("div", class_="total").string.strip() if money.find("div", class_="total") else "0.0"
            price = float(price_str.encode('utf-8').decode('ascii', 'ignore').replace("€", "").strip())
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

            writer.add_document(name=name, url_inf=url_inf, price=price, discount=discount, score=score, description=description, release_date=release_date,
                                developer=developer.name, genres=",".join(video_games_genres), plataform=plataform.name, store=store.name)

            video_games_list, dic_genres = create_video_game(name, url_inf, url_img, price, discount, score, description, release_date, developer, 
                                                            video_games_genres, dic_genres, plataform, store, video_games_list)
    
    create_video_games(video_games_list, dic_genres, total_genres, store)
    writer.commit()
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
    # traducimos los géneros
    i = 0
    for i in range(len(video_games_genres)):
        if video_games_genres[i] in genre_traductor:
            video_games_genres[i] = genre_traductor[video_games_genres[i]]

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
def populate_eneba(dir_index, num_pages, dic_developers, total_genres, dic_genres, dic_plataforms):
    video_games_list = []
    eneba_total_genres = []
    store = Store.objects.create(name="Eneba")
    print("START ENEBA WEB SCRAPPING")

    ix = open_dir(dir_index)
    writer = ix.writer()

    for page in range(1, num_pages+1):
        request = urllib.request.Request(f"https://www.eneba.com/es/store/games?page={page}&platforms[]=BETHESDA&platforms[]=BLIZZARD&platforms[]=EPIC_GAMES&platforms[]=GOG&platforms[]=ORIGIN&platforms[]=OTHER&platforms[]=STEAM&platforms[]=UPLAY&regions[]=global&sortBy=POPULARITY_DESC&types[]=game", 
                                         headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
        f = urllib.request.urlopen(request, timeout=3)
        s = BeautifulSoup(f, 'lxml')
        s_video_games = s.find("div", class_="JZCH_t").find_all("div", class_="WpvaUk")

        for s_video_game in s_video_games:
            name = s_video_game.find("div", class_="lirayz").text.strip()
            url_inf = "https://www.eneba.com" + s_video_game.a['href'].strip()
            url_img = s_video_game.img['src'].strip()
            money = s_video_game.find("div", class_="Lyw0wM")
            price_parse = money.find("span", class_="L5ErLT").string.split(",") if money else ["0", "00"]
            price = float(price_parse[0] + "." + price_parse[1][:2])
            discount_str = money.find("div", class_="PIG8fA")
            discount = int(discount_str.string.split(" ")[1].replace("%", "").strip()) if discount_str else 0

            request2 = urllib.request.Request(url_inf, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
            try:
                f2 = urllib.request.urlopen(request2, timeout=3)
            except HTTPError as e:
                if e.code == 429:  # too many requests error
                    print("Too many request. Waiting before trying again...")
                    time.sleep(10)  # esperar 10 segundos
                    f2 = urllib.request.urlopen(request2, timeout=3)
                else:
                    raise
            s2 = BeautifulSoup(f2, 'lxml')

            s_score = s2.find("div", class_="mMO4Vf").text.strip() if s2.find("div", class_="mMO4Vf") else "0.0"
            score = float(s_score) * 2          # multiplicamos por 2 para que este en una escala sobre 10
            s_description = s2.find("div", class_="tq3wly")
            description = "".join(list(s_description.stripped_strings)) if s_description else ""
            s_release_date = s2.find("div", class_="URplpg", string="Fecha de lanzamiento").next_sibling
            release_date = datetime.strptime(str(s_release_date.string.strip()), '%d de %B de %Y') if s_release_date else None
            developer, dic_developers = get_developer_eneba(s2, dic_developers)
            video_games_genres, eneba_total_genres = get_genres_eneba(s2, eneba_total_genres)
            plataform, dic_plataforms = get_plataform_eneba(s2, dic_plataforms)

            writer.add_document(name=name, url_inf=url_inf, price=price, discount=discount, score=score, description=description, release_date=release_date,
                                developer=developer.name, genres=",".join(video_games_genres), plataform=plataform.name, store=store.name)
            
            video_games_list, dic_genres = create_video_game(name, url_inf, url_img, price, discount, score, description, release_date, developer, 
                                                            video_games_genres, dic_genres, plataform, store, video_games_list)
    
    create_video_games(video_games_list, dic_genres, [genre for genre in eneba_total_genres if genre not in total_genres], store)
    writer.commit()
    print("FINISH ENEBA WEB SCRAPPING")


# función auxiliar para obtener el desarrollador de un videojuego
def get_developer_eneba(s2, dic_developers):
    s_developer = s2.find("div", class_="URplpg", string="Desarrolladores")
    if s_developer:
        developer_string = s_developer.next_sibling.string.strip()
    else:
        developer_string = "Unknown"

    if developer_string not in dic_developers:
        developer = Developer.objects.create(name=developer_string)
        dic_developers[developer_string] = developer
    developer = dic_developers[developer_string]
    return developer, dic_developers


# función auxiliar para obtener los géneros de un videojuego
def get_genres_eneba(s2, eneba_total_genres):
    video_games_genres = []

    s_genres = s2.find("ul",class_="aoHRvN")
    if s_genres:
        for li in s_genres:
            genre = str(list(li.stripped_strings)[0]).lower()
            video_games_genres.append(genre)
    # traducimos los géneros
    i = 0
    for i in range(len(video_games_genres)):
        if video_games_genres[i] in genre_traductor:
            video_games_genres[i] = genre_traductor[video_games_genres[i]]

    for genre in video_games_genres:
        if genre not in eneba_total_genres:
            eneba_total_genres.append(genre)
    return video_games_genres, eneba_total_genres


# función auxiliar para obtener la plataforma de un videojuego
def get_plataform_eneba(s2, dic_plataforms):
    s_plataform = list(s2.find_all("strong",class_="cEhl9f"))[1]
    if s_plataform:
        plataform_string = str(s_plataform.string.strip()).lower()
    else:
        plataform_string = "Unknown"
    
    if plataform_string not in dic_plataforms:
        plataform = Plataform.objects.create(name=plataform_string)
        dic_plataforms[plataform_string] = plataform
    plataform = dic_plataforms[plataform_string]
    return plataform, dic_plataforms


