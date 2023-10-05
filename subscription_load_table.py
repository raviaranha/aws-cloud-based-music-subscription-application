from decimal import Decimal
import json
import boto3

def load_movies(music_list, dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')#,
                                #endpoint_url="http://localhost:8000")
    table = dynamodb.Table('subscription')
    for music in music_list["songs"]:

        try:
            title = music['title']
            artist = music['artist']
            year = int(music['year'])
            web_url = music['web_url']
            img_url = music['img_url']
            print("Adding music:", title, artist, year, web_url, img_url)
            table.put_item(Item=music)

        except KeyError:
            print("Missing key in data:", music)
            continue



if __name__ == '__main__':
    with open("s1.json") as json_file:
        music_list = json.load(json_file, parse_float=Decimal)
    load_movies(music_list)
