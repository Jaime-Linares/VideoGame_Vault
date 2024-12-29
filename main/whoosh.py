from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from main.models import Video_game



# función que busca los videojuegos cuya fecha de lanzamiento se encuentre en el rango especificado
def video_games_in_period(dir_index, start_date, end_date):
    video_games = []
    start_date_whoosh = start_date.strftime('%Y%m%d')
    end_date_whoosh = end_date.strftime('%Y%m%d')

    ix = open_dir(dir_index)
    with ix.searcher() as searcher:
        date_range = '[' + start_date_whoosh + ' TO ' + end_date_whoosh + ']'
        query = QueryParser("release_date", ix.schema).parse(date_range)
        results = searcher.search(query, limit=None)

        for r in results:
            video_game = Video_game.objects.all().get(url_inf=r['url_inf'])
            video_games.append(video_game)

    return video_games


# función para buscar los videojuegos que sean de un precio menor o igual al especificado
def video_games_selected_max_price(dir_index, max_price):
    video_games = []

    ix = open_dir(dir_index)
    with ix.searcher() as searcher:
        query = QueryParser("price", ix.schema).parse('[0 TO ' + str(max_price) + ']')
        results = searcher.search(query, limit=None)

        for r in results:
            video_game = Video_game.objects.all().get(url_inf=r['url_inf'])
            video_games.append(video_game)

    return video_games


# función para buscar los videojuegos más relevantes que contengan la/s palabra/s especificada/s en el título o descripción
def video_games_with_words(dir_index, words):
    video_games = []

    ix = open_dir(dir_index)
    with ix.searcher() as searcher:
        query = MultifieldParser(["name", "description"], ix.schema, group=OrGroup).parse(str(words))
        results = searcher.search(query, limit=10)

        for r in results:
            video_game = Video_game.objects.all().get(url_inf=r['url_inf'])
            video_games.append(video_game)

    return video_games


# función para buscar los videojuegos más relevantes que pertenezcan a un género y que contengan la/s palabra/s especificada/s en el título
def video_games_by_genre_and_words(dir_index, genre, words):
    video_games = []
    genre = '"' + genre.name + '"'  # se ponen comillas porque hay géneros que tienen más de una palabra

    ix = open_dir(dir_index)
    with ix.searcher() as searcher:
        query = MultifieldParser(["genres", "name"], ix.schema).parse(genre + " AND " + str(words))
        results = searcher.search(query, limit=10)

        for r in results:
            video_game = Video_game.objects.all().get(url_inf=r['url_inf'])
            video_games.append(video_game)

    return video_games


# función para buscar los videojuegos más relevantes que contengan la frase especificada en la descripción
def video_games_by_description(dir_index, sentence):
    video_games = []

    ix = open_dir(dir_index)
    with ix.searcher() as searcher:
        query = QueryParser("description", ix.schema).parse('"'+ sentence + '"')
        results = searcher.search(query, limit=10)

        for r in results:
            video_game = Video_game.objects.all().get(url_inf=r['url_inf'])
            video_games.append(video_game)

    return video_games

