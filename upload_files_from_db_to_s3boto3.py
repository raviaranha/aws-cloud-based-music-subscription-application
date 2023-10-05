import logging
import boto3
from botocore.exceptions import ClientError
#from pprint import pprint
import os
import requests

def get_music_url(dynamodb=None):

    #connect to s3
    s3_client = boto3.client('s3')

    #connect to dynamodb
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('music')

    #get a list of items from the table object
    table_items = table.scan()
    
    for item in table_items['Items']:
        img_url = item['img_url']
        #filename = os.path.basename(img_url)
        filename = item['artist']
        print("filename: ", filename)
        print("img_url: ", img_url)

        #get image based on the url
        response = requests.get(img_url)

        #save url to s3
        if response.status_code == 200:
            s3_client.put_object(Bucket="artistimages0104",
                        Key=filename,
                        Body=response.content)
            print("Uploaded")
        else:
            print("Error uploading")

get_music_url()
