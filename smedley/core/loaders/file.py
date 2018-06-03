import json

from simple_settings import settings

from .base import BaseTaskLoader


class FileTaskLoader(BaseTaskLoader):

    def _load_tasks(self):
        file_path = settings.TASKS_FILE_PATH
        with open(file_path, 'r') as file_data:
            return json.load(file_data)
