from app_auth import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from twython import Twython


class Message():
    message = ''
    photo = ''
    photo_caption = ''

    def __init__(self, message_type='', photo='', photo_caption=''):
        self.message_type = message_type
        self.photo = photo
        self.photo_caption


    def create_tweet_message_time(self, time_data):
        morning = ''
        sentence = ''
        time_str = str(time_data[0]) + ':' + str(time_data[1]) + ' ' + time_data[2]

        if time_data[2].lower() == 'am':
            greeting = 'morning'
            sentence = 'Have a good one on Earth! :)'

        elif time_data[2]:
            if (time_data[0] <= 12) and (time_data[0] <= 5):
                greeting = 'afternoon'
                sentence = 'How is (or was) your morning? :)'
            elif (time_data[0] > 5) and (time_data[0] < 12):
                greeting = 'night'
                sentence = 'How is (or was) your day on Earth?. :)'

        self.message = 'Good {}, it is {} here on Mars. {}'.format(greeting, time_str, sentence)


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
        twitter.update_status(status=self.message)


    def post_message_with_photo_on_twitter(self):
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        photo = open(self.photo, 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=self.message, media_ids=[response['media_id']])