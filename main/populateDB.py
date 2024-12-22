# encoding:utf-8
from main.models import Developer, Genre, Plataform, Store, Video_game
from bs4 import BeautifulSoup
import os, re, ssl, lxml, urllib.request
from datetime import datetime
# lineas para evitar error SSL
from markdown_it.rules_inline import link
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context



# --- FUNCIÓN PRINCIPAL PARA CARGAR LOS DATOS ------------------------------------------------------------------------------
def populate():
    # borramos todos los registros de la base de datos
    Developer.objects.all().delete()
    Genre.objects.all().delete()
    Plataform.objects.all().delete()
    Store.objects.all().delete()
    Video_game.objects.all().delete()
    # cargamos los datos desde instant-gaming
    populate_instant_gaming()
    # cargamos los datos desde eneba
    populate_eneba()


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
def populate_instant_gaming():
    return None



# --- FUNCIONES ENEBA ------------------------------------------------------------------------------------------------------
def populate_eneba():
    return None


