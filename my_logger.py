import logging
from datetime import datetime


def set_my_logger(logger_name):
    logger = logging.getLogger(logger_name)
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
    return logger
