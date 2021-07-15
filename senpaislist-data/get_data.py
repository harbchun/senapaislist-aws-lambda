import os
import json
import uuid
import boto3 
import collections

from utils import times, scrape

# AWS variables
AWS_BUCKET_REGION = os.environ.get('AWS_BUCKET_REGION')
AWS_DATA_BUCKET_NAME = os.environ.get('AWS_DATA_BUCKET_NAME')
AWS_IMAGES_BUCKET_NAME = os.environ.get('AWS_IMAGES_BUCKET_NAME')

# const variables
THE_FORBIDDEN_GENRE_2=os.environ.get('THE_FORBIDDEN_GENRE_2')
THE_FORBIDDEN_GENRE_1=os.environ.get('THE_FORBIDDEN_GENRE_1')
YEAR = times.get_current_year()
SEASON = times.get_current_season()
DIR_JSON = '/tmp/'
FILE_EXTENSION_JSON = '.json'
DIR_JPG = '/tmp/'
FILE_EXTENSION_JPG = '.jpg'

# test variables
test_season = 'winter'

def lambda_handler(event, context):
    # S3
    s3 = boto3.resource('s3', region_name=AWS_BUCKET_REGION)
    s3_client = boto3.client('s3', region_name=AWS_BUCKET_REGION)
    # get the bucket object
    data_bucket = s3.Bucket(AWS_DATA_BUCKET_NAME)
    images_bucket = s3.Bucket(AWS_IMAGES_BUCKET_NAME)
    # get the objects (files)
    data_objects = data_bucket.objects.filter(Prefix='2013/fall')
    # list of anime ids current in the bucket
    anime_ids_in_bucket = [json_content['mal_id'] for json_content in [json.loads(file.get()['Body'].read().decode('utf-8')) for file in data_objects]]
    dups = [item for item, count in collections.Counter(anime_ids_in_bucket).items() if count > 1]
    
    return {
        'statusCode': 200,
        'body': json.dumps(dups)
    }
    
    # JIKAN
    # get ids for current year and season
    anime_ids_from_api = scrape.retrieve_anime_ids(YEAR, test_season)
    
    # get difference of two lists
    relevant_anime_ids = list(set(anime_ids_from_api) - set(anime_ids_in_bucket))
    
    for anime_id in relevant_anime_ids:
        anime_data = scrape.retrieve_anime_data(anime_id) # Jikan api json reponse for this anime
        
        # FILTER
        genres_dict_list = anime_data.get("genres", [])
        genres = [x.get("name", '') for x in genres_dict_list]
        if THE_FORBIDDEN_GENRE_1 in genres or THE_FORBIDDEN_GENRE_2 in genres:
            continue
        
        # FILE
        random_file_name = str(uuid.uuid4())
        anime_data['file_id'] = random_file_name
        
        # IMAGE
        # random_image_id = s3utils.random_uuid()
        # anime_data['image_id'] = random_image_id # save the image id to the JPG file
        # anime_image_url = anime_data.get('image_url', None)

        # # save the image locally
        # if anime_image_url:
        #     image_url_request = requests.get(anime_image_url, stream = True)

        #     if image_url_request.status_code == 200:
        #         # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        #         image_url_request.raw.decode_content = True
        #         # Open a local file with wb ( write binary ) permission.
        #         with open(DIR_JPG+random_image_id+FILE_EXTENSION_JPG,'wb') as anime_image:
        #             shutil.copyfileobj(image_url_request.raw, anime_image)
        #     else:
        #         print('Image Couldn\'t be retreived')
        #     # save to s3 bucket
        #     s3_client.upload_file(DIR_JPG+random_image_id+FILE_EXTENSION_JPG, AWS_IMAGES_BUCKET_NAME, str(year)+'/'+season+'/'+random_image_id+FILE_EXTENSION_JPG)
        #     # remove the jpg file once it is done uploaded  
        #     os.remove(DIR_JPG+random_image_id+FILE_EXTENSION_JPG)
        

        # DATA
        # temporarily create the json file 
        random_anime_id = str(uuid.uuid4())
        anime_data['anime_id'] = random_anime_id
        with open(DIR_JSON+random_file_name+FILE_EXTENSION_JSON, 'w') as s3_file:
            json.dump(anime_data, s3_file)
        s3_client.upload_file(DIR_JSON+random_file_name+FILE_EXTENSION_JSON, AWS_DATA_BUCKET_NAME, str(YEAR)+'/'+test_season+'/'+random_file_name+FILE_EXTENSION_JSON)
        # remove the json file once it is done uploaded
        os.remove(DIR_JSON+random_file_name+FILE_EXTENSION_JSON)
        
    return {
        'statusCode': 200,
        'body': json.dumps(dups)
    }
    