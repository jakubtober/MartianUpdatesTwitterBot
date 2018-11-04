import bot
import json
from my_logger import set_my_logger

logger = set_my_logger(__name__)

my_bot = bot.Bot()
my_bot.choose_message()

logger.info('-----------------------------------------------------------------------------------------')
