import mock
import pytest
from simple_settings import settings

from smedley.core.config import DriverConfig
from smedley.core.schemas import BASE_TASK_SCHEMA
from .conftest import MockBaseTaskLoader
from ..base import BaseTaskLoader
from ..exceptions import (
    InvalidTask,
    InvalidTaskLoaderClass,
    TaskDriverNotFound,
    TaskLoaderNotFound
)


class TestBaseTaskLoader:

    def setup(self):
        self.loader = BaseTaskLoader()
        settings.LOADERS = {
            'test': (
                'smedley.core.loaders.tests.conftest.MockBaseTaskLoader'
            )
        }
        settings.DRIVERS = {
            'test': 'test'
        }

    def test_validate_loader(self):
        result = BaseTaskLoader.validate_loader(loader=self.loader)
        assert result is None

    def test_validate_loader_error(self):
        with pytest.raises(InvalidTaskLoaderClass):
            BaseTaskLoader.validate_loader(loader=None)

    def test_get_loader(self):
        loader = self.loader.get_loader('test')
        assert isinstance(loader, MockBaseTaskLoader)

    def test_get_loader_error(self):
        settings.LOADERS = {
            'test': (
                'smedley.core.loaders.tests.'
                'conftest.MockInvalidBaseTaskLoader'
            )
        }
        with pytest.raises(InvalidTaskLoaderClass):
            self.loader.get_loader('test')

    def test_get_loader_not_found(self):
        with pytest.raises(TaskLoaderNotFound):
            self.loader.get_loader('abc')

    def test_validate_driver(self):
        result = self.loader.validate_driver(driver_name='test')
        assert result is None

    def test_validate_driver_not_registered(self):
        with pytest.raises(TaskDriverNotFound):
            self.loader.validate_driver(driver_name='abc')

    def test_get_driver(self, task):
        driver_name = self.loader.get_driver(task=task)
        assert driver_name == 'test'

    def test_get_driver_invalid_task(self, task):
        task.driver = None
        with pytest.raises(InvalidTask):
            self.loader.get_driver(task=task)

    @mock.patch.object(DriverConfig, '_load_config')
    @mock.patch.object(DriverConfig, 'get_task_schema')
    def test_get_data(self, get_task_schema, _load_config, task):
        get_task_schema.return_value = {}
        _load_config.return_value = None
        assert self.loader.get_data(
            task=task,
            driver='test'
        ) == {}

    @pytest.mark.parametrize('field,value', [
        ('name', ''),
        ('driver', ''),
        ('steps', None),
    ])
    @mock.patch.object(DriverConfig, '_load_config')
    @mock.patch.object(DriverConfig, 'get_task_schema')
    def test_get_data_invalid(
        self,
        get_task_schema,
        _load_config,
        field,
        value,
        task
    ):
        get_task_schema.return_value = BASE_TASK_SCHEMA
        _load_config.return_value = None
        task[field] = value
        with pytest.raises(InvalidTask):
            self.loader.get_data(
                task=task,
                driver='test'
            )

    def test__load_tasks(self):
        with pytest.raises(Exception):
            self.loader._load_tasks()

    @mock.patch.object(DriverConfig, '_load_config')
    @mock.patch.object(DriverConfig, 'get_task_schema')
    @mock.patch.object(BaseTaskLoader, '_load_tasks')
    def test_load_tasks(
        self,
        _load_tasks,
        get_task_schema,
        _load_config,
        tasks
    ):
        _load_tasks.return_value = tasks
        get_task_schema.return_value = BASE_TASK_SCHEMA
        _load_config.return_value = None
        result = self.loader.load_tasks()
        assert len(result) == len(tasks)

    def test_load_tasks_error(self):
        with pytest.raises(Exception):
            self.loader.load_tasks()
