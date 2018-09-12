from app_auth import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from twython import Twython
import json
import random

TIME = 'time'
LOCATION_AND_TIME ='location_and_time'
WEATHER = 'weather'
message_types = [TIME, LOCATION_AND_TIME, WEATHER]

class Message():

    hashtags = [
        '#Mars',
        '#space',
        '#RoverCuriosity',
        '#Curiosity',
        '#planets',
        '#space',
        '#science',
        '#curiosityrover',
        '#nasa',
        '#ESA',
        '#robot',
        '#stars',
        '#world'
    ]

    def __init__(self, my_data=[], message_type='', photo='', photo_caption=''):
        self.message_type = message_type
        self.photo = photo
        self.photo_caption = photo_caption
        posts_history_file = open('posts_history.json', 'r')
        self.posts_history = json.load(posts_history_file)
        self.my_data = my_data

    def __str__(self):
        return "{}. {}, {}".format(self.message, self.photo, self.photo_caption)

    def create_tweet_message_time(self):
        sentence = ''
        greeting = ''
        time_str = str(self.my_data.time[0]) + ':' + str(self.my_data.time[1]) + ' ' \
        + self.my_data.time[2]

        if self.my_data.time[2].lower() == 'am':
            greeting = 'morning'
            sentence = 'Have a good one on Earth! :)'
        else:
            if self.my_data.time[0] >= 12 or self.my_data.time[0] <= 5:
                greeting = 'afternoon'
                sentence = 'How is (or was) your morning? :)'
            elif self.my_data.time[0] > 5 and self.my_data.time[0] < 12:
                greeting = 'night'
                sentence = 'How is (or was) your day on Earth?. :)'
        self.message = 'Good {}, it is {} here on Mars. {}'.format(greeting, time_str, sentence)
        self.message_type = TIME

    def create_tweet_message_location_and_time(self):
        self.message = 'Hi, just to let you know im in{}. It is {}here on Mars.'.format(
            self.my_data.location_str,
            self.my_data.time_str
        )
        self.message_type = LOCATION_AND_TIME

    def create_tweet_message_weather(self):
        self.message = 'Report on {} (sol: {}). Air temp max: {} C, air temp min: {} C. {}.'.format(
            self.my_data.last_day_data['earths_date'],
            self.my_data.last_day_data['sol'],
            self.my_data.last_day_data['air_temp_max'],
            self.my_data.last_day_data['air_temp_min'],
            self.my_data.last_day_data['radiation_level']
        )
        self.message_type = WEATHER

    def test_tweet_in_cmd_before_posting(self):
        if self.message:
            print(self.message)
        else:
            print('You need to create message first. ')
        if self.photo:
            print(self.photo)
        else:
            print('Photo not specified.')

    def post_on_twitter(self):
        shuffeled_hashtags_str = ''

        for number in range(8):
            random_tag = random.choice(self.hashtags)
            shuffeled_hashtags_str += random_tag + ' '
            self.hashtags.remove(random_tag)

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        twitter.update_status(status=self.message + ' ' + shuffeled_hashtags_str)

        posts_history_file = open('posts_history.json', 'r+')
        history_data = json.load(posts_history_file)
        history_data[self.my_data.last_day_data['sol']] = self.message_type

        with open('posts_history.json', 'w') as posts_history_file:
            json.dump(history_data, posts_history_file)

    def post_message_with_photo_on_twitter(self):
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        photo = open(self.photo, 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=self.message + self.hastags, media_ids=[response['media_id']])
