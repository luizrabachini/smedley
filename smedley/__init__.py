import logging

from simple_settings import settings


logging.config.dictConfig(settings.LOGGING)
