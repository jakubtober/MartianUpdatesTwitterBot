import bot
import json
from time import sleep

# time between cycles in seconds
hours_to_wait = 24
minutes_to_wait = 0
seconds_to_wait = 0
time_to_wait = (hours_to_wait * 60 * 60) + (minutes_to_wait *60) + (seconds_to_wait)

while True:
    my_bot = bot.Bot()
    my_bot.choose_message()
    print('-----------------------------------------------------------------------------------------')
    print('Next cycle will be run in {} h {} min {} sec'.format(str(hours_to_wait), str(minutes_to_wait), str(seconds_to_wait)))
    print('So {} seconds.'.format(str(time_to_wait)))
    sleep(time_to_wait)
