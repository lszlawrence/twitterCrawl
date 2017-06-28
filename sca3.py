# -*- coding: utf-8 -*-
import oauth2
import urllib
import json
import re
from time import gmtime, strftime
import unirest
CONSUMER_KEY = "2R4kJEiWZw4W3hEVjRX0hXVcG"
CONSUMER_SECRET = "cq4z0KWPmLjUTOTmEl2M6zGIgCc90QctmFfTmE15YDlkjXX0Ac"
global_count = 0
# TODO Sentiment analysis


def sentitment_test(text):
    global global_count
    global_count += 1
    api_url = "https://community-sentiment.p.mashape.com/text/"
    headers = {
        "X-Mashape-Key": "ymVD3PG3WOmshjP6YD0ebRmPYiU6p1oXLkwjsnz1AkxDS6K2wG",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    params = {
        "txt": text
    }

    response = unirest.post(api_url, headers=headers, params=params)
    return response.body['result']['sentiment']


def oauth_req(url):
    http_method = "GET"
    post_body = ""
    http_headers = None
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    client = oauth2.Client(consumer)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    content = urllib.unquote(content)
    content_dict = json.loads(content)
    returned_data = "id,user_name,text,date,time,timespan,sentiment\n"
    for tweet in content_dict["statuses"]:
        id_str = tweet["id_str"]
        created_at = tweet["created_at"]
        utc_offset = 0
        if tweet["user"]["utc_offset"] is not None:
            utc_offset = int(tweet["user"]["utc_offset"])/3600
        hour = int(created_at[11:13])+utc_offset
        date_offset = 0
        if hour < 0:
            hour += 24
            date_offset = -1
            print "Back one day"

        timespan = ""
        if hour < 6:
            timespan = "Night"
        elif hour < 12:
            timespan = "Morning"
        elif hour < 17:
            timespan = "Afternoon"
        else:
            timespan = "Evening"

        day = str(int(created_at[8:10]) + date_offset)
        time = str(hour) + ":" + created_at[14:16]
        date = day + '/' + created_at[4:7] + '/' + created_at[-2:]

        text = re.sub("[^A-Z0-9a-z !'/@#.:]", '', tweet["text"])
        user_name = re.sub("[^A-Z0-9a-z !'/@#.:]", '', tweet["user"]["name"])
        sentiment = sentitment_test(text)
        cleared = "%s,%s,%s,%s,%s,%s,%s,\n" % (id_str, user_name, text, date, time, timespan, sentiment)
        returned_data += cleared

    return returned_data.encode('utf-8')


def save_data(url):
    gun_control_tweets = oauth_req(url)
    # Get the current time.
    file_path = strftime("%Y%m%d%H%M%S", gmtime())
    output = open("data/%s.csv" % file_path, "w+")
    output.write(gun_control_tweets)
    output.close()

request_url = "https://api.twitter.com/1.1/search/tweets.json?"
request_url += "count=100"
request_url += "&result_type=recent"
request_url += "&q=Casino%20River%20Hotel%20"

save_data(request_url)