import os, traceback, shelve, spacy
from main.models import Video_game, Genre, Plataform, Developer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from langdetect import detect


# carga los modelos de spaCy para inglés y español
nlp_en = spacy.load("en_core_web_md")
nlp_es = spacy.load("es_core_news_md")

# pesos para los atributos
DESCRIPTION_WEIGHT = 1.5
GENRES_WEIGHT = 1.75
NAME_WEIGHT = 1.5



# --- FUNCIONES PARA GENERAR Y GUARDAR LAS RECOMENDACIONES -------------------------------------------------------------------------
# función que genera las recomendaciones y las guarda en su archivo correspondiente
def generate_and_save_recommendations(dir_rs_data):
    try:
        # vemos si los archivos de recomendación están generados y si es así, los borramos
        archivos = [dir_rs_data+".bak", dir_rs_data+".dat", dir_rs_data+".dir"]
        for archivo in archivos:
            if os.path.exists(archivo):
                os.remove(archivo)
        
        print("STARTING TO SAVE THE RECOMMENDATION SYSTEM")
        # generamos los vectores de los videojuegos
        video_game_ids, vectors = generate_video_games_vectors()
        # calculamos la matriz de similitud utilizando la similitud del coseno
        print("Calculating the similarity matrix")
        similarity_matrix = cosine_similarity(vectors)
        # guardamos las recomendaciones
        print("Saving the recommendations")
        with shelve.open(dir_rs_data) as db:
            for idx, video_game_id in enumerate(video_game_ids):
                similar_indices = similarity_matrix[idx].argsort()[::-1]
                recommended_ids = [video_game_ids[i] for i in similar_indices if i != idx][:4]
                db[str(video_game_id)] = recommended_ids
        print(f"RECOMMENDATION SYSTEM SAVED SUCCESSFULLY")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()


# función que genera vectores de características combinando todos los atributos de los videojuegos
def generate_video_games_vectors():
    print("Generating vectors for video games")
    video_games_ids = []
    valid_video_games = []
    name_vectors = []
    description_vectors = []

    video_games = Video_game.objects.all()
    print(f"Total number of video games found: {len(video_games)}")

    for idx, video_game in enumerate(video_games):
        if not video_game.description:
            print(f"Warning! The game with name {video_game.name} and id {video_game.id} has no description, it will be skipped")
            continue
        try:
            # detectamos el idioma y procesamos el título
            nlp_model_name = get_spacy_model(video_game.name, video_game.id)
            name_vectors.append(nlp_model_name(video_game.name).vector)
            # detectamos el idioma y procesamos la descripción
            nlp_model_desc = get_spacy_model(video_game.description, video_game.id)
            description_vectors.append(nlp_model_desc(video_game.description).vector)
            # añadimos el videojuego a la lista de juegos válidos y guardamos su id
            valid_video_games.append(video_game)
            video_games_ids.append(video_game.id)
        except Exception as e:
            print(f"Error processing video game {video_game.id}: {e}")
            traceback.print_exc()

    print(f"{len(valid_video_games)} valid video games were processed out of a total of {len(video_games)} video games")

    # concatenamos los vectores de características de los videojuegos
    try:
        name_vectors = np.array(name_vectors)
        description_vectors = np.array(description_vectors)
        genre_vectors, platform_vectors, developer_vectors = encode_categorical_attributes(valid_video_games)
        numerical_attributes = normalize_numerical_attributes(valid_video_games)
        print("Concatenating the vectors")
        # multiplicamos por el peso correspondiente a cada atributo, si no se especifica se asume 1
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
        print(f"Error concatenating vectors: {e}")
        traceback.print_exc()
        raise

    return video_games_ids, combined_vectors


# función que sirve para detectar el idioma de un texto y devolver el modelo de spaCy correspondiente
def get_spacy_model(text, video_game_id):
    try:
        language = detect(text)
        if language == "es":
            return nlp_es
        elif language == "en":
            return nlp_en
    except Exception:
        print(f"Error detecting language for game with id {video_game_id}. We will use English by default.")
        pass  # si no se puede detectar el idioma, usar inglés por defecto
    return nlp_en


# función que codifica los atributos categóricos de los videojuegos (géneros, plataforma y desarrollador)
# transformándolos en vectores binarios
def encode_categorical_attributes(video_games):
    genre_vectors, platform_vectors, developer_vectors = [], [], []

    all_genres = list(Genre.objects.values_list("name", flat=True))
    all_platforms = list(Plataform.objects.values_list("name", flat=True))
    all_developers = list(Developer.objects.values_list("name", flat=True))
    for video_game in video_games:
        # codificamos los géneros como vector binario
        game_genres = [genre.name for genre in video_game.genres.all()]
        genre_vectors.append([1 if genre in game_genres else 0 for genre in all_genres])
        # codificamos la plataforma como vector binario
        platform_vectors.append([1 if platform == video_game.plataform.name else 0 for platform in all_platforms])
        # codificamos desarrollador como vector binario
        developer_vectors.append([1 if developer == video_game.developer.name else 0 for developer in all_developers])

    return np.array(genre_vectors), np.array(platform_vectors), np.array(developer_vectors)


# función que normaliza los atributos numéricos de los videojuegos (precio y puntuación)
# dejándolos en un rango de 0 a 1 mediante MinMaxScaler
def normalize_numerical_attributes(video_games):
    prices = [video_game.price for video_game in video_games]
    scores = [video_game.score for video_game in video_games]

    scaler = MinMaxScaler()
    return scaler.fit_transform(np.array([prices, scores]).T)



# --- FUNCIONES PARA OBTENER Y CARGAR LAS RECOMENDACIONES -------------------------------------------------------------------------
# función que obtiene las recomendaciones para un videojuego específico
def get_recommendations_for_game(game_id, dir_rs_data, recommendations):
    if recommendations is None:
        recommendations = load_recommendations(dir_rs_data)
    return recommendations.get(game_id)


# función que carga las recomendaciones desde el archivo donde se encuentran
def load_recommendations(dir_rs_data):
    try:
        with shelve.open(dir_rs_data) as db:
            return {int(key): value for key, value in db.items()}
    except Exception as e:
        print(f"Error loading recommendations: {e}")
        traceback.print_exc()
        return {}

