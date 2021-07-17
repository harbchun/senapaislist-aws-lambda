import os
import json
import uuid
import boto3 
import requests
import shutil

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

# S3
s3 = boto3.resource('s3', region_name=AWS_BUCKET_REGION)
s3_client = boto3.client('s3', region_name=AWS_BUCKET_REGION)
# get the bucket object
data_bucket = s3.Bucket(AWS_DATA_BUCKET_NAME)
images_bucket = s3.Bucket(AWS_IMAGES_BUCKET_NAME)
# get the objects (files)
data_objects = data_bucket.objects.filter(Prefix=str(YEAR)+'/'+SEASON)

def main(event, context):
    # list of anime ids current in the bucket
    anime_ids_in_bucket = [
        json_content['mal_id'] for json_content in \
            [json.loads(file.get()['Body'].read().decode('utf-8')) for file in data_objects]
    ]

    # JIKAN
    # get ids for current year and season
    anime_ids_from_api = scrape.get_anime_ids(YEAR, SEASON)
    
    # get difference of two lists
    relevant_anime_ids = list(set(anime_ids_from_api) - set(anime_ids_in_bucket))
    
    for anime_id in relevant_anime_ids:
        anime_data = scrape.retrieve_anime_data(anime_id) # Jikan api json reponse for this anime
        
        # FILE
        random_file_name = str(uuid.uuid4())
        anime_data['file_id'] = random_file_name
        
        # IMAGE
        random_image_id = str(uuid.uuid4())
        anime_data['image_id'] = random_image_id # save the image id to the JPG file
        anime_image_url = anime_data.get('image_url', None)

        # save the image locally
        if anime_image_url:
            image_url_request = requests.get(anime_image_url, stream = True)

            if image_url_request.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                image_url_request.raw.decode_content = True
                # Open a local file with wb ( write binary ) permission.
                with open('/tmp/'+random_image_id+'.jpg','wb') as anime_image:
                    shutil.copyfileobj(image_url_request.raw, anime_image)
            else:
                print('Image for %s:  Couldn\'t be retreived' % random_file_name)
            # save to s3 bucket
            s3_client.upload_file('/tmp/'+random_image_id+'.jpg', AWS_IMAGES_BUCKET_NAME, str(YEAR)+'/'+SEASON+'/'+random_image_id+'.jpg')
            # remove the jpg file once it is done uploaded  
            os.remove('/tmp/'+random_image_id+'.jpg')
        

        # DATA
        random_anime_id = str(uuid.uuid4())
        anime_data['anime_id'] = random_anime_id

        # get data
        anime_data_json = json.dumps(anime_data)

        # add the data
        curr_season_object = s3.Object(AWS_DATA_BUCKET_NAME, str(YEAR)+'/'+SEASON+'/'+random_file_name+'.json')
        curr_season_object.put(Body=anime_data_json)
        
    return {
        'statusCode': 200,
        'body': 'Success!'
    }
    