import time
import urllib3
import json

def retrieve_anime_ids(year, season):
    time.sleep(4)
    http = urllib3.PoolManager()
    seasonResponse = http.request("GET", "https://api.jikan.moe/v3/season/" + str(year) + "/" + season)

    seasonData = seasonResponse.data
    jobj = json.loads(seasonData)

    if not jobj['anime']: return ''

    return [x['mal_id'] for x in jobj['anime']]
        
def retrieve_anime_data(anime_id):
    time.sleep(4)
    http = urllib3.PoolManager()
    animeResponse = http.request("GET", "https://api.jikan.moe/v3/anime/" + str(anime_id))

    return json.loads(animeResponse.data)