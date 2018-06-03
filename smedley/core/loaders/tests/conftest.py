import json

import pytest

from ..base import BaseTaskLoader


class MockBaseTaskLoader(BaseTaskLoader):
    pass


class MockInvalidBaseTaskLoader:
    pass


@pytest.fixture
def tasks_file(tmpdir, tasks):
    content = json.dumps(tasks)
    temp_file = tmpdir.mkdir('tests').join('tasks.json')
    temp_file.write(content)
    return str(temp_file)
