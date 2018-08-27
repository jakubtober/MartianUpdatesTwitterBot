import messages
import data


class Bot():
    def __init__(self):
        my_data = data.RoverData()
        my_data.get_remaining_mars_rems_data()
        my_data.get_time()

        my_message = messages.Message(my_data=my_data)

        print('\n')
        print('Test message 1:')
        my_message.create_tweet_message_time()
        my_message.test_tweet_in_cmd_before_posting()

        print('\n')
        print('Test message 2:')
        my_message.create_tweet_message_location()
        my_message.test_tweet_in_cmd_before_posting()

        print('\n')
        print('Test message 3:')
        my_message.create_tweet_message_weather()
        my_message.test_tweet_in_cmd_before_posting()
