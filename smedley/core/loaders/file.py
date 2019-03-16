import json
import yaml

from simple_settings import settings

from .base import BaseTaskLoader


class FileTaskLoader(BaseTaskLoader):

    def _load_tasks(self):
        file_path = settings.TASKS_FILE_PATH
        with open(file_path, 'r') as file_data:
            file_format = file_path.split('.')[-1]
            if file_format == 'json':
                return json.load(file_data)
            elif file_format in ['yaml', 'yml']:
                return yaml.load(file_data)
