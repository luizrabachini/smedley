import pytest
from simple_settings import settings

from smedley.core.loaders import FileTaskLoader


class TestFileLoader:

    def setup(self):
        self.loader = FileTaskLoader()

    def test__load_tasks(self, tasks_file, tasks):
        settings.TASKS_FILE_PATH = tasks_file
        loaded_tasks = self.loader._load_tasks()
        assert len(loaded_tasks) == len(tasks)

    def test__load_tasks_file_not_found(self):
        settings.TASKS_FILE_PATH = '/some/path/data.json'
        with pytest.raises(FileNotFoundError):
            self.loader._load_tasks()
