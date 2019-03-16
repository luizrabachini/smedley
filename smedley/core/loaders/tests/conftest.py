import json
import yaml

import pytest

from ..base import BaseTaskLoader


class MockBaseTaskLoader(BaseTaskLoader):
    pass


class MockInvalidBaseTaskLoader:
    pass


@pytest.fixture
def tasks_file_json(tmpdir, tasks):
    content = json.dumps(tasks)
    temp_file = tmpdir.mkdir('tests').join('tasks.json')
    temp_file.write(content)
    return str(temp_file)


@pytest.fixture
def tasks_file_yaml(tmpdir, tasks):
    content = yaml.dump(tasks)
    temp_file = tmpdir.mkdir('tests').join('tasks.yaml')
    temp_file.write(content)
    return str(temp_file)
