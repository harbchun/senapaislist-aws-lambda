import os
import json
import boto3 

from utils import times

# AWS variables
AWS_BUCKET_REGION = os.environ.get('AWS_BUCKET_REGION')
AWS_DATA_BUCKET_NAME = os.environ.get('AWS_DATA_BUCKET_NAME')
AWS_BROADCAST_TIMES_BUCKET_NAME = os.environ.get('AWS_BROADCAST_TIMES_BUCKET_NAME')

# const variables
THE_FORBIDDEN_GENRE_1=os.environ.get('THE_FORBIDDEN_GENRE_1')
THE_FORBIDDEN_GENRE_2=os.environ.get('THE_FORBIDDEN_GENRE_2')
YEAR = times.get_current_year()
SEASON = times.get_current_season()
LAST_YEAR = times.get_last_year()
LAST_SEASON = times.get_last_season()

def main(event, context):
    s3 = boto3.resource('s3', region_name=AWS_BUCKET_REGION)
    # get the bucket objects
    data_bucket = s3.Bucket(AWS_DATA_BUCKET_NAME)
    broadcast_times_bucket = s3.Bucket(AWS_BROADCAST_TIMES_BUCKET_NAME)

    return str(YEAR) + SEASON + str(LAST_YEAR) + LAST_SEASON 

if __name__ == "__main__":   
    main('', '')