from app_auth import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from twython import Twython
import json


class Message():
    my_data = []
    message = ''
    photo = ''
    photo_caption = ''
    hastags = ' #Mars #space #Rover #Curiosity #planets #science'
    posts_history = []

    def __init__(self, my_data=[], message_type='', photo='', photo_caption=''):
        self.message_type = message_type
        self.photo = photo
        self.photo_caption
        posts_history_file = open('posts_history.json', 'r')
        self.posts_history = json.load(posts_history_file)
        self.my_data = my_data


    def __str__(self):
        return "{}. {}, {}".format(self.message, self.photo, self.photo_caption)


    def create_tweet_message_time(self):
        sentence = ''
        greeting = ''
        time_str = str(self.my_data.time[0]) + ':' + str(self.my_data.time[1]) + ' ' + self.my_data.time[2]

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


    def create_tweet_message_location(self):
        self.message = 'Hi im in{}.'.format(self.my_data.location_str)


    def create_tweet_message_location_and_time(self):
        self.message = 'Hi, just to let you know im in{}. It is {}here on Mars.'.format(self.my_data.location_str, self.my_data.time_str)


    def create_tweet_message_weather(self):
        self.message = 'Report on {} (sol: {}). Air temp max: {} C, air temp min: {} C. {}.'.format(
            self.my_data.last_day_data['earths_date'],
            self.my_data.last_day_data['sol'],
            self.my_data.last_day_data['air_temp_max'],
            self.my_data.last_day_data['air_temp_min'],
            self.my_data.last_day_data['radiation_level']
        )


    def choose_message_type(self):
        pass


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
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        twitter.update_status(status=self.message + self.hastags)


    def post_message_with_photo_on_twitter(self):
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        photo = open(self.photo, 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=self.message + self.hastags, media_ids=[response['media_id']])
