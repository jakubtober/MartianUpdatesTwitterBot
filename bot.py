import messages
import data
import json
import random


class Bot():
    sample_messages = {}
    message_to_post = None

    def __init__(self):
        print('Bot initalized.')
        print('Collecting data...')
        my_data = data.RoverData()
        my_data.get_remaining_mars_rems_data()
        my_data.get_time()

        time_message = messages.Message(my_data=my_data)
        location_message = messages.Message(my_data=my_data)
        location_and_time_message = messages.Message(my_data=my_data)
        weather_message = messages.Message(my_data=my_data)

        time_message.create_tweet_message_time()
        location_message.create_tweet_message_location()
        location_and_time_message.create_tweet_message_location_and_time()
        weather_message.create_tweet_message_weather()

        self.sample_messages['time'] = time_message
        self.sample_messages['location'] = location_message
        self.sample_messages['location_and_time'] = location_and_time_message
        self.sample_messages['weather'] = weather_message


    def print_sample_messages_in_cmd(self):
        print('Sample messages:' + '\n')
        print(self.sample_messages['time'])
        print(self.sample_messages['location'])
        print(self.sample_messages['location_and_time'])
        print(self.sample_messages['weather'])


    def choose_message(self):
        sols = []

        posts_history_file = open('posts_history.json')
        history_data = json.load(posts_history_file)

        for key in history_data.keys():
            sols.append(int(key))

        last_days_history = [history_data[str(sol)] for sol in sorted(sols, reverse=True)]

        print('Last post was about sol: ' + str(max(sols)))
        print('Post type: ' + history_data[str(max(sols))])
        print('Last posts types: ' + str(last_days_history))

        available_message_types_for_new_post = [key for key in self.sample_messages.keys()]
        random.shuffle(available_message_types_for_new_post)
        print('Types availabe for new post: ' + str(available_message_types_for_new_post))

        for message_type in available_message_types_for_new_post:
            if message_type not in last_days_history[:4]:
                self.message_to_post = self.sample_messages[message_type]
                print('Type for new message: ' + str(message_type))
                break

        print('New potential message to post: ' + str(self.message_to_post))
