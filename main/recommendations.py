import os, traceback, shelve, spacy
from main.models import Video_game, Genre, Plataform, Developer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from langdetect import detect


# Pesos para los atributos
DESCRIPTION_WEIGHT = 3.0
GENRES_WEIGHT = 2.0
NAME_WEIGHT = 1.5

# Carga los modelos de spaCy para inglés y español
nlp_en = spacy.load("en_core_web_md")
nlp_es = spacy.load("es_core_news_md")



def get_spacy_model(text):
    """
    Devuelve el modelo spaCy correspondiente al idioma detectado.
    """
    try:
        lang = detect(text)
        if lang == "es":
            return nlp_es
        elif lang == "en":
            return nlp_en
    except Exception:
        pass  # Si no se puede detectar el idioma, usar inglés por defecto
    return nlp_en


def encode_categorical_attributes(games):
    """
    Codifica los géneros, plataformas y desarrolladores manualmente como vectores binarios.
    """
    all_genres = list(Genre.objects.values_list("name", flat=True))
    all_platforms = list(Plataform.objects.values_list("name", flat=True))
    all_developers = list(Developer.objects.values_list("name", flat=True))

    genre_vectors, platform_vectors, developer_vectors = [], [], []
    for game in games:
        # Codificar géneros como vector binario
        game_genres = [genre.name for genre in game.genres.all()]
        genre_vectors.append([1 if genre in game_genres else 0 for genre in all_genres])

        # Codificar plataforma como vector binario (única plataforma por juego)
        platform_vectors.append([1 if platform == game.plataform.name else 0 for platform in all_platforms])

        # Codificar desarrollador como vector binario (único desarrollador por juego)
        developer_vectors.append([1 if developer == game.developer.name else 0 for developer in all_developers])

    return np.array(genre_vectors), np.array(platform_vectors), np.array(developer_vectors)


def normalize_numerical_attributes(games):
    """
    Normaliza atributos numéricos como precio y puntuación.
    """
    prices = [game.price for game in games]
    scores = [game.score for game in games]

    scaler = MinMaxScaler()
    return scaler.fit_transform(np.array([prices, scores]).T)


def generate_game_vectors():
    """
    Genera vectores de características combinando todos los atributos de los videojuegos.
    """
    print("Iniciando generación de vectores...")
    games = Video_game.objects.all()
    game_ids = []
    description_vectors = []
    name_vectors = []

    valid_games = []

    print(f"Total de juegos encontrados: {len(games)}")

    for idx, game in enumerate(games):
        if not game.description or not game.name:
            print(f"Advertencia: El juego {game.id} (índice {idx}) no tiene descripción o nombre. Se omitirá.")
            continue

        try:
            # Detectar idioma y procesar descripción
            nlp_model_desc = get_spacy_model(game.description)
            description_vectors.append(nlp_model_desc(game.description).vector)

            # Detectar idioma y procesar título
            nlp_model_name = get_spacy_model(game.name)
            name_vectors.append(nlp_model_name(game.name).vector)

            valid_games.append(game)
            game_ids.append(game.id)

        except Exception as e:
            print(f"Error al procesar el juego {game.id}: {e}")
            traceback.print_exc()

    print(f"Se procesaron {len(valid_games)} juegos válidos de un total de {len(games)} juegos.")

    try:
        description_vectors = np.array(description_vectors)
        name_vectors = np.array(name_vectors)

        genre_vectors, platform_vectors, developer_vectors = encode_categorical_attributes(valid_games)
        numerical_attributes = normalize_numerical_attributes(valid_games)

        print("Verificando tamaños de arrays:")
        print(f"Descripción: {description_vectors.shape}")
        print(f"Nombre: {name_vectors.shape}")
        print(f"Géneros: {genre_vectors.shape}")
        print(f"Plataformas: {platform_vectors.shape}")
        print(f"Desarrolladores: {developer_vectors.shape}")
        print(f"Atributos numéricos: {numerical_attributes.shape}")

        print("Concatenando vectores...")
        combined_vectors = np.hstack(
            [
                description_vectors * DESCRIPTION_WEIGHT,
                name_vectors * NAME_WEIGHT,
                genre_vectors * GENRES_WEIGHT,
                platform_vectors,
                developer_vectors,
                numerical_attributes,
            ]
        )

    except Exception as e:
        print(f"Error al concatenar vectores: {e}")
        traceback.print_exc()
        raise

    return game_ids, combined_vectors


def generate_and_save_recommendations(dir_rs_data):
    """
    Genera las recomendaciones y las guarda en el archivo shelve.
    """
    try:
        # archivos que se generan
        archivos = [dir_rs_data+".bak", dir_rs_data+".dat", dir_rs_data+".dir"]
        # Eliminar archivos previos
        for archivo in archivos:
            if os.path.exists(archivo):
                os.remove(archivo)
        
        print("Generando vectores de videojuegos...")

        # Generar vectores
        game_ids, vectors = generate_game_vectors()

        print("Calculando matriz de similitud...")
        similarity_matrix = cosine_similarity(vectors)

        print("Guardando recomendaciones en shelve...")
        with shelve.open(dir_rs_data) as db:
            for idx, game_id in enumerate(game_ids):
                similar_indices = similarity_matrix[idx].argsort()[::-1]
                recommended_ids = [game_ids[i] for i in similar_indices if i != idx][:4]
                db[str(game_id)] = recommended_ids

        print(f"Recomendaciones guardadas en {dir_rs_data}")

    except Exception as e:
        print(f"Error inesperado: {e}")
        traceback.print_exc()


def load_recommendations(dir_rs_data):
    """
    Carga las recomendaciones desde el archivo shelve.
    """
    try:
        with shelve.open(dir_rs_data) as db:
            return {int(key): value for key, value in db.items()}
    except Exception as e:
        print(f"Error al cargar las recomendaciones: {e}")
        traceback.print_exc()
        return {}


def get_recommendations_for_game(game_id, dir_rs_data, recommendations):
    """
    Obtiene las recomendaciones para un videojuego específico.
    """
    if recommendations is None:
        recommendations = load_recommendations(dir_rs_data)
    return recommendations.get(game_id, [])

