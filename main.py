import messages
import data

# Main program (example instructions)

# time = data.get_time()
# my_message = messages.Message(photo='./photos/jpg/2114-rhaz-2.jpg')
# my_message.create_tweet_message_time(time)
# my_message.test_tweet_in_cmd_before_posting()
# my_message.post_message_with_photo_on_twitter()

my_data = data.RoverData()
my_data.get_time()
my_new_message = messages.Message(photo='./photos/jpg/2115-navcam-8.jpg')
my_new_message.create_tweet_message_location_and_time(my_data)
my_new_message.test_tweet_in_cmd_before_posting()
my_new_message.post_message_with_photo_on_twitter()
