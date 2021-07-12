import json
from utils import syoboi

jp_title_tid_dict = syoboi.get_jp_title_tid_dict() 

# TODO: to be used when the key is changed to TID from MAL_ID
def get_existing_tids(data_objects):
    title_jp_in_bucket = [
        json_content.get('title_japanese', '') for json_content in \
            [json.loads(file.get()['Body'].read().decode('utf-8')) for file in data_objects]
    ]

    return [jp_title_tid_dict[title] for title in (jp_title_tid_dict.keys() & title_jp_in_bucket)]

def get_existing_tid_malid_dict(data_objects):
    jp_title_malid_dict = {
        json_content.get('title_japanese', ''): json_content.get('mal_id', '') \
            for json_content in \
            [json.loads(file.get()['Body'].read().decode('utf-8')) for file in data_objects]
    }

    return {
        jp_title_tid_dict[title] :jp_title_malid_dict[title] \
            for title in (jp_title_tid_dict.keys() & jp_title_malid_dict.keys())
    }