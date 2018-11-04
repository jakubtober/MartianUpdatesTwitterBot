import bot
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

date_now = datetime.now()
logs_filename = '{}_{}_{}.log'.format(
    date_now.year,
    date_now.month,
    date_now.day,
)
file_handler = logging.FileHandler('./logs/{}'.format(logs_filename))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logger_formatter)

logger.addHandler(file_handler)

my_bot = bot.Bot()
my_bot.choose_message()

logger.info('-----------------------------------------------------------------------------------------')
