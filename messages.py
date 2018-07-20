from app_auth import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from twython import Twython


class Message():
    message = ''
    photo = ''
    photo_caption = ''
    hastags = ' #Mars #space #Rover #Curiosity #planets #science'

    def __init__(self, message_type='', photo='', photo_caption=''):
        self.message_type = message_type
        self.photo = photo
        self.photo_caption


    def __str__(self):
        return "{}. {}, {}".format(self.message, self.photo, self.photo_caption)


    def create_tweet_message_time(self, time_data):
        sentence = ''
        greeting = ''
        time_str = str(time_data[0]) + ':' + str(time_data[1]) + ' ' + time_data[2]

        if time_data[2].lower() == 'am':
            greeting = 'morning'
            sentence = 'Have a good one on Earth! :)'
        else:
            if time_data[0] >= 12 or time_data[0] <= 5:
                greeting = 'afternoon'
                sentence = 'How is (or was) your morning? :)'
            elif time_data[0] > 5 and time_data[0] < 12:
                greeting = 'night'
                sentence = 'How is (or was) your day on Earth?. :)'

        self.message = 'Good {}, it is {} here on Mars. {}'.format(greeting, time_str, sentence)


    def create_tweet_message_location(self, my_data):
        self.message = 'Hi im in {}. It is '.format(my_data.location_str)


    def create_tweet_message_location_and_time(self, my_data):
        self.message = 'Hi, just to let you know im in{}. It is {}here on Mars.'.format(my_data.location_str, my_data.time_str)


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
