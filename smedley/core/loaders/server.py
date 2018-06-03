import logging

import requests
from simple_settings import settings

from .base import BaseTaskLoader


logger = logging.getLogger(__name__)


class ServerTaskLoader(BaseTaskLoader):

    def _load_tasks(self):
        server_url = settings.TASKS_MASTER_SERVER
        server_timeout = settings.TASKS_MASTER_SERVER_TIMEOUT

        try:
            response = requests.get(server_url, timeout=server_timeout)
            return response.json()
        except:
            logger.exception(
                'Error on request tasks from server {}'.format(server_url)
            )
            raise
