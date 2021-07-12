import os
import json
import boto3 

from utils import times, syoboi, helper

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

    ##### LAST SEASON #####
    # get the objects (files)
    last_season_data_objects = data_bucket.objects.filter(Prefix=str(LAST_YEAR)+'/'+LAST_SEASON)
    
    # TODO: use this instead of the one below
    # list of japanese titles currently in the data bucket
    # existing_tid_list = helper.get_existing_tids(data_objects)

    # get dictionary with k,v pairs of existing (in the bucket) anime tid, malid 
    last_season_existing_dict = helper.get_existing_tid_malid_dict(last_season_data_objects)

    # get data
    last_season_broadcast_times = syoboi.get_season_broadcast_times(last_season_existing_dict)
    last_season_json_object = json.dumps(last_season_broadcast_times)

    # add the data
    last_season_object = s3.Object(AWS_BROADCAST_TIMES_BUCKET_NAME, str(LAST_YEAR)+'/'+LAST_SEASON+'.json')
    last_season_object.put(Body=last_season_json_object)
    ##### LAST SEASON #####


    ##### CURRENT SEASON #####
    # get the objects (files)
    curr_season_data_objects = data_bucket.objects.filter(Prefix=str(YEAR)+'/'+SEASON)

    # get dictionary with k,v pairs of existing (in the bucket) anime tid, malid 
    curr_season_existing_dict = helper.get_existing_tid_malid_dict(curr_season_data_objects)

    # get data
    curr_season_broadcast_times = syoboi.get_season_broadcast_times(curr_season_existing_dict)
    curr_season_json_object = json.dumps(curr_season_broadcast_times)

    # add the data
    curr_season_object = s3.Object(AWS_BROADCAST_TIMES_BUCKET_NAME, str(YEAR)+'/'+SEASON+'.json')
    curr_season_object.put(Body=curr_season_json_object)
    ##### CURRENT SEASON #####

    return 'Success!'

if __name__ == "__main__":   
    main('', '')