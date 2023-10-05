import datetime
from flask import Flask, render_template, request, redirect, flash, g, jsonify
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import os
import requests


import logging
from logging import StreamHandler

app = Flask(__name__)


app.logger.addHandler(StreamHandler())
app.logger.setLevel(logging.INFO)

is_user_login = False

headers = {"Content-Type": "application/json",
           "webapp": "e9ms8TkASoa1uhvPWc0lX9xXIluTayJg4v2uRmhW"}
login_api_url = "https://7wfhv7kauc.execute-api.us-east-1.amazonaws.com/app/login_research"
register_api_url = "https://6keqwnml9c.execute-api.us-east-1.amazonaws.com/app/register"
query_api_url = "https://3aic26701c.execute-api.us-east-1.amazonaws.com/app/query"
subscribe_api_url = "https://i8b8yxe2r5.execute-api.us-east-1.amazonaws.com/app/subscribe"
unsubscribe_api_url = "https://sldrrccbl4.execute-api.us-east-1.amazonaws.com/app/unsubscribe"

# show login page by default


@app.route('/')
def main():
    return render_template('login2.html')


@app.route('/logout')
def logout():
    return render_template('login2.html')


# login functionality
@app.route('/login2', methods=['POST'])
def login2():
    email = request.form['email']
    password = request.form['password']

    body = {
        "email": email,
        "password": password
    }

    response = requests.post(login_api_url, headers=headers, json=body)
    output = response.json()
    # msg = ""
    # user = ""

    # s3_client = boto3.client('s3')
    # dynamodb = boto3.resource('dynamodb')
    # login_table = dynamodb.Table('login')

    # # get a list of items from the table object
    # login_table_items = login_table.scan()

    # for item in login_table_items['Items']:
    #     item_email = item['email']
    #     item_password = item['password']

    #     if item_email == email and item_password == password:
    #         msg = "Email found"+email
    #         user = item['user_name']

    #         # show subscrption
    #         subscription_table = dynamodb.Table('subscription').scan()[
    #             'Items']  # handle exception when this is blank
    #         subscription_table_and_images = []

    #         response_from_s3 = s3_client.list_objects_v2(
    #                 Bucket="artistimages0104")

    #         for line in subscription_table:
    #             artist = line['artist']

    #             for obj in response_from_s3['Contents']:
    #                 if obj['Key'] == artist:
    #                     # Get the URL of the S3 object
    #                     img_url = s3_client.generate_presigned_url('get_object',
    #                                                         Params={'Bucket': "artistimages0104",
    #                                                                 'Key': obj['Key']},
    #                                                         ExpiresIn=3600)

    #             line_data = line['title']+", " + \
    #                 line['artist']+", "+str(line['year'])
    #             new_subscription_and_images = {
    #                 "name": line_data, "img_url": img_url}
    #             subscription_table_and_images.append(
    #                 new_subscription_and_images)

    #         # return redirect('home', subscription_table = subscription_table_and_images)
    #         return render_template('home2.html', subscription_table=subscription_table_and_images,
    #                                user=user)

    # if msg == "":
    #     msg = "email or password is incorrect"
    #     return render_template('login2.html', msg=msg)

    if 'Email found:' in output.get('body')['msg']:
        return render_template('home2.html', subscription_table=output.get('body')['subscription_table'],
                               user=output.get('body')['user'])

    else:
        return render_template('login2.html', msg="email or password is incorrect")


@app.route('/register2')
def register2():
    return render_template('register2.html')

# @app.route('/register_validation')


@app.post('/register_validation2')
def register_validation2():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    body = {
        "email": email,
        "password": password,
        "username": username
    }

    response = requests.post(register_api_url, headers=headers, json=body)
    output = response.json()

    # msg = ""
    # dynamodb = boto3.resource('dynamodb')
    # login_table = dynamodb.Table('login')

    # # get a list of items from the table object
    # login_table_items = login_table.scan()

    # for item in login_table_items['Items']:
    #     item_email = item['email']
    #     if item_email == email:
    #         msg = "Email already available. Log in instead"
    #         return render_template('register2.html', msg=msg)

    # if msg == "":
    #     # add to database
    #     table = dynamodb.Table('login')
    #     table.put_item(Item={
    #         "email": email,
    #         "password": password,
    #         "user_name": username
    #     })
    #     msg = "Successfully registered. Log in"
    #     return render_template('login2.html', msg=msg)
    # return render_template('register2.html')

    print(output.get('body'))
    if 'Email already available' in output.get('body')['msg']:
        return render_template('register2.html', msg=output.get('body')['msg'])

    elif 'Successfully registered' in output.get('body')['msg']:
        return render_template('login2.html', msg=output.get('body')['msg'])

    else:
        return render_template('register2.html', msg=output.get('body')['msg'])


@app.route('/home2')
def home2():
    return render_template('home2.html')


@app.route('/query2', methods=['POST'])
def query_results2():
    print("------------------------------->>>>>>>>>>>", request.get_json())
    year = request.get_json().get('year')
    artist = request.get_json().get('artist')
    title = request.get_json().get('title')

    # add here

    body = {
        "year": year,
        "artist": artist,
        "title": title
    }

    response = requests.post(query_api_url, headers=headers, json=body)
    output = response.json()

    # print("<----------- get_json() output ------->\n", year, artist, title)

    # if title == "":
    #     title = False
    # if year == "":
    #     year = False
    # if artist == "":
    #     artist = False
    # filter = None
    # queried_items = []

    # # set filter criterea
    # if title and year and artist:
    #     filter = Attr('title').eq(title) & Attr(
    #         'year').eq(year) & Attr('artist').eq(artist)
    # elif title and year:
    #     filter = Attr('title').eq(title) & Attr('year').eq(year)
    # elif title and artist:
    #     filter = Attr('title').eq(title) & Attr('artist').eq(artist)
    # elif year and artist:
    #     filter = Attr('year').eq(year) & Attr('artist').eq(artist)
    # elif title:
    #     filter = Attr('title').eq(title)
    # elif year:
    #     filter = Attr('year').eq(year)
    # elif artist:
    #     filter = Attr('artist').eq(artist)

    # s3_client = boto3.client('s3')
    # dynamodb = boto3.resource('dynamodb')
    # music_table = dynamodb.Table('music')

    # # filter out the queries items
    # if title or year or artist:
    #     queried_items = music_table.scan(FilterExpression=filter)['Items']

    # # add the data and image in dictionary format
    # queried_items_and_images = []

    # response_from_s3 = s3_client.list_objects_v2(
    #     Bucket="artistimages0104")

    # print("response_from_s3:\n", response_from_s3)

    # for line in queried_items:
    #     artist = line['artist']

    #     for obj in response_from_s3['Contents']:
    #         if obj['Key'] == artist:
    #             # Get the URL of the S3 object
    #             img_url = s3_client.generate_presigned_url('get_object',
    #                                                        Params={'Bucket': "artistimages0104",
    #                                                                'Key': obj['Key']},
    #                                                        ExpiresIn=3600)
    #             print("---- img_url in queried_items --->\n", img_url)

    #     line_data = line['title']+", "+line['artist']+", "+line['year']
    #     new_items_and_images = {"name": line_data, "img_url": img_url}
    #     queried_items_and_images.append(new_items_and_images)

    # subscription_table = dynamodb.Table('subscription').scan()['Items']
    # subscription_table_and_images = []

    # for line in subscription_table:
    #     artist = line['artist']
    #     # response_from_s3 = s3_client.list_objects_v2(
    #     #     Bucket="artistimages0104", Prefix=artist)
    #     for obj in response_from_s3['Contents']:
    #         if obj['Key'] == artist:
    #             # Get the URL of the S3 object
    #             img_url = s3_client.generate_presigned_url('get_object',
    #                                                        Params={'Bucket': "artistimages0104",
    #                                                                'Key': obj['Key']},
    #                                                        ExpiresIn=3600)

    #     line_data = line['title']+", "+line['artist']+", "+str(line['year'])
    #     new_subscription_and_images = {"name": line_data, "img_url": img_url}
    #     subscription_table_and_images.append(new_subscription_and_images)

    # print(queried_items_and_images)
    # if len(queried_items) == 0:
    #     return render_template('home2.html', query_table=queried_items_and_images,
    #                            subscription_table=subscription_table_and_images,
    #                            title=title,
    #                            artist=artist,
    #                            year=year,
    #                            qmsg="empty query or item not found")
    # else:
    #     return render_template('home2.html', query_table=queried_items_and_images,
    #                            subscription_table=subscription_table_and_images,
    #                            title=title,
    #                            artist=artist,
    #                            year=year)

    if output.get('body')['len_q'] == 0:
        return render_template('home2.html', query_table=output.get('body')['query_table'],
                               subscription_table=output.get(
                                   'body')['subscription_table'],
                               title=output.get('body')['title'],
                               artist=output.get('body')['artist'],
                               year=output.get('body')['year'],
                               qmsg="empty query or item not found")

    else:
        return render_template('home2.html', query_table=output.get('body')['query_table'],
                               subscription_table=output.get(
                                   'body')['subscription_table'],
                               title=output.get('body')['title'],
                               artist=output.get('body')['artist'],
                               year=output.get('body')['year'])


@app.route('/subscribe2', methods=['POST'])
def subscribe2():

    print("------------------------------->>>>>>>>>>>", request.get_json())
    year = request.get_json().get('year')
    artist = request.get_json().get('artist')
    title = request.get_json().get('title')
    subscribed_item = request.get_json().get('subscribed_item')

    body = {
        "year": year,
        "artist": artist,
        "title": title,
        "subscribed_item": subscribed_item
    }

    response = requests.post(subscribe_api_url, headers=headers, json=body)
    output = response.json()

    # s3_client = boto3.client('s3')
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('subscription')

    # print("<----------- get_json() output in subscribe ------->\n",
    #       year, artist, title, subscribed_item)

    # subscribed_title = subscribed_item.rsplit(
    #     ',', 2)[-3]  # .strip()#[-3].strip()
    # filter = Attr('title').eq(subscribed_title)
    # music_table = dynamodb.Table('music')
    # # print(music_table.scan(FilterExpression=filter)['Items'])
    # subscribed_items = music_table.scan(FilterExpression=filter)['Items'][0]
    # table.put_item(Item=subscribed_items)
    # subscription_table = dynamodb.Table('subscription').scan()[
    #     'Items']  # handle exception when this is blank
    # subscription_table_and_images = []

    # for line in subscription_table:
    #     artist = line['artist']
    #     response_from_s3 = s3_client.list_objects_v2(
    #         Bucket="artistimages0104", Prefix=artist)
    #     for obj in response_from_s3['Contents']:
    #         if obj['Key'] == artist:
    #             # Get the URL of the S3 object
    #             img_url = s3_client.generate_presigned_url('get_object',
    #                                                        Params={'Bucket': "artistimages0104",
    #                                                                'Key': obj['Key']},
    #                                                        ExpiresIn=3600)

    #             line_data = line['title']+", " + \
    #                 line['artist']+", "+str(line['year'])
    #             new_subscription_and_images = {
    #                 "name": line_data, "img_url": img_url}
    #             subscription_table_and_images.append(
    #                 new_subscription_and_images)

    # queried_items_and_images = []  # if coded, also add s3 images.

    # print("queried_items_and_images:\n", queried_items_and_images)
    # print("subscription_table_and_images:\n", subscription_table_and_images)

    # return render_template('home2.html',
    #                        query_table=queried_items_and_images,
    #                        subscription_table=subscription_table_and_images,
    #                        title=title,
    #                        year=year,
    #                        artist=artist)

    return render_template('home2.html',
                           query_table=output.get('body')['query_table'],
                           subscription_table=output.get(
                               'body')['subscription_table'],
                           title=output.get('body')['title'],
                           artist=output.get('body')['artist'],
                           year=output.get('body')['year'])


@app.route('/unsubscribe2', methods=['POST'])
def unsubscribe2():

    print("------------------------------->>>>>>>>>>>", request.get_json())
    year = request.get_json().get('year')
    artist = request.get_json().get('artist')
    title = request.get_json().get('title')
    unsubscribed_item = request.get_json().get('unsubscribed_item')

    body = {
        "year": year,
        "artist": artist,
        "title": title,
        "unsubscribed_item": unsubscribed_item
    }

    response = requests.post(unsubscribe_api_url, headers=headers, json=body)
    output = response.json()

    # s3_client = boto3.client('s3')
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('subscription')

    # print("<----------- get_json() output in unsubscribe ------->\n",
    #       year, artist, title, unsubscribed_item)

    # unsubscribed_title = unsubscribed_item.rsplit(',', 2)[-3]

    # print("Deleting subscription:", unsubscribed_title)
    # table.delete_item(Key={'title': unsubscribed_title})

    # subscription_table = dynamodb.Table('subscription').scan()[
    #     'Items']
    # subscription_table_and_images = []

    # print("subscriptions w/o images:\n", subscription_table)

    # for line in subscription_table:
    #     artist = line['artist']
    #     response_from_s3 = s3_client.list_objects_v2(
    #         Bucket="artistimages0104", Prefix=artist)
    #     for obj in response_from_s3['Contents']:
    #         if obj['Key'] == artist:
    #             # Get the URL of the S3 object
    #             img_url = s3_client.generate_presigned_url('get_object',
    #                                                        Params={'Bucket': "artistimages0104",
    #                                                                'Key': obj['Key']},
    #                                                        ExpiresIn=3600)

    #             line_data = line['title']+", " + \
    #                 line['artist']+", "+str(line['year'])
    #             new_subscription_and_images = {
    #                 "name": line_data, "img_url": img_url}
    #             subscription_table_and_images.append(
    #                 new_subscription_and_images)

    #             print("\nentered here\n")

    # queried_items_and_images = []  # if coded, also add s3 images.

    # print("queried_items_and_images:\n", queried_items_and_images)
    # print("subscription_table_and_images:\n", subscription_table_and_images)

    # return render_template('home2.html',
    #                        query_table=queried_items_and_images,
    #                        subscription_table=subscription_table_and_images,
    #                        title=title,
    #                        year=year,
    #                        artist=artist)

    return render_template('home2.html',
                           query_table=output.get('body')['query_table'],
                           subscription_table=output.get('body')['subscription_table'],
                           title=output.get('body')['title'],
                           artist=output.get('body')['artist'],
                           year=output.get('body')['year'])


if __name__ == '__main__':
    # if you change, change in home for register also.
    # app.run(host='127.0.0.1', port=8080, debug=True)

    # ----------------------------------------------------------------------------------> CHANGE WHEN UPLOADING TO CLOUD
    app.run(host='0.0.0.0', port=5000)
