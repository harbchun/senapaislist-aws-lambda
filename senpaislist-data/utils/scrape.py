import time
import requests
import os

def get_anime_ids(year, season):
    time.sleep(4)

    THE_FORBIDDEN_GENRE_1=os.environ.get('THE_FORBIDDEN_GENRE_1')
    THE_FORBIDDEN_GENRE_2=os.environ.get('THE_FORBIDDEN_GENRE_2')
    tfg = (THE_FORBIDDEN_GENRE_1, THE_FORBIDDEN_GENRE_2)

    anime_list_url = 'https://api.jikan.moe/v3/season/' + str(year) + '/' + season
    anime_list_response = requests.get(anime_list_url)
    anime_list_dict = anime_list_response.json()

    if not anime_list_dict['anime']: return ''

    anime_id_list = []
    for anime in anime_list_dict['anime']:
        genres = tuple([genre['name'] for genre in anime['genres']])
        if any(genre in genres for genre in tfg):
            continue
        anime_id_list.append(anime['mal_id'])

    return anime_id_list
        
def retrieve_anime_data(anime_id):
    time.sleep(4)

    anime_data_url = 'https://api.jikan.moe/v3/anime/' + str(anime_id)
    anime_data_response = requests.get(anime_data_url)
    anime_data_dict = anime_data_response.json()

    return anime_data_dict