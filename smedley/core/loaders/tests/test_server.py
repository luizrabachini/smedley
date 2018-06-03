import mock
import pytest
from requests.exceptions import Timeout

from smedley.core.loaders import ServerTaskLoader


class TestServerTaskLoader:

    def setup(self):
        self.loader = ServerTaskLoader()

    @mock.patch('smedley.core.loaders.server.requests.get')
    def test__load_tasks(self, mocked_get, tasks):
        mocked_get.return_value = mock.Mock(
            status_code=200,
            json=lambda: tasks
        )
        loaded_tasks = self.loader._load_tasks()
        assert len(loaded_tasks) == len(tasks)

    @mock.patch('smedley.core.loaders.server.requests.get')
    def test__load_tasks_timeout(self, mocked_get):
        mocked_get.side_effect = Timeout()
        with pytest.raises(Timeout):
            self.loader._load_tasks()
