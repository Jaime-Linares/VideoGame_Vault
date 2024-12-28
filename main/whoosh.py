from whoosh.index import open_dir
from whoosh.qparser import QueryParser
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

