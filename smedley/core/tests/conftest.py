import pytest

from smedley.core.executors.base import BaseTaskExecutor


class ValidConfig:

    schema = {'name': str}
    executor = 'test'


class ValidExecutor(BaseTaskExecutor):

    pass


@pytest.fixture
def valid_config():
    return ValidConfig()


@pytest.fixture
def valid_schema():
    return {'url': str}


@pytest.fixture
def valid_executor():
    return ValidExecutor()
