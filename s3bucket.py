
#bucket ARN: arn:aws:s3:::vama-prod-audit


import logging
import boto3
from botocore.exceptions import ClientError
import os

import logging

from datetime import timedelta

import datetime

bucket_name = "vama-prod-audit"
object_name = "chat_messages-20240425.csv"
aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key =os.getenv("AWS_SECRET_ACCESS_KEY")

def start():
    client = None
    #bucket_name = "vama-prod-audit"

    client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
    return client


def write_to_s3(full_filename,bucket_name,object_name):
    client = start()
    #s3.download_file('vama-prod-audit','agora_recording_files-20240616.csv','abc.csv')
    response = client.put_object(
    ACL="private",
    Body=full_filename,
    Bucket=bucket_name,
    ServerSideEncryption="AES256",
    Key=object_name,
    Metadata={"env": "qa", "owner": "binary guy"},
    )
    logger.debug(response)


def download_from_s3():
    full_filename = (
    f"audit-files"
    f"/agora_recording_files-20240616.csv"
    )
    bucket_name = "vama-prod-audit"
    object_name = "agora_recording_files-20240616.csv"




# def upload_file(file_name, bucket, object_name=None,s3_client=None):
#     """Upload a file to an S3 bucket

#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = os.path.basename(file_name)

#     # Upload the file
#     s3_client = s3_client
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True


def list_s3(bucket_name):
    client = start()
    response = client.list_objects_v2(
        Bucket=bucket_name,
    )
    print(response)
    #logger.debug(type(response))

def get_objects_s3(bucket_name):
    client = start()
    paginator = client.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=bucket_name, Delimiter='/')
    #print(result)
    dt = datetime.datetime.now() - timedelta(days=1)
    search_pattern = f"Contents[?to_string(LastModified)>='\"{dt}\"'].Key"
    #print(search_pattern)
    for key_data in result.search(search_pattern):
        print(key_data)
        client.download_file(bucket_name,
                                  key_data,
                                  f"{key_data}")
        return key_data


# dt = datetime.datetime.now() - timedelta(days=2)
# now = dt.strftime("%Y%m%d")
# print(now)

# chat_file = "chat_messages-"+str(now) +".csv"
# audio_file =   "agora_recording-"+str(now) +".csv"

# client = start()
# client.download_file(bucket_name,chat_file,f"{chat_file}")

import pandas as pd



# def handle(self, *args, **options):
#     list_bucket = options.get('list')
#     get_bucket = options.get('get')
#     if list_bucket:
#         self.list_s3()
#     elif get_bucket:
#         self.get_objects_s3()



bucket_name = 'vama-prod-audit'
#client = start()
#get_objects_s3(bucket_name)
list_s3(bucket_name)

#client = start()

#client.download_file(bucket_name,"agora_recording_files-20240704.csv","download1.csv")

#response = client.list_objects_v2(Bucket='vama-prod-audit')

#print(response.keys())

#import schedule

from time import sleep

from Audio import audio_thread
from Chat import chat_thread

def download_both(bucket_name):
    try:
        dt = datetime.datetime.now() - timedelta(days=2)
        now = dt.strftime("%Y%m%d")
        print("this is downloading now",now)
        chat_file = "chat_messages-"+str(now) +".csv"
        audio_file =   "agora_recording_files-"+str(now) +".csv"

        client = start()
        client.download_file(bucket_name,chat_file,f"{chat_file}")
        client.download_file(bucket_name,audio_file,f"{audio_file}")
        sleep(10)
        audio_thread(audio_file)
        sleep(10)
        #chat_thread(chat_file)

        #thread2
    except Exception as e:
        print(e)
        #time.sleep(1800)  ## wait for 30 mins 
    


download_both(bucket_name)
