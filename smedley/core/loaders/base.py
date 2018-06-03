from attrdict import AttrDict
import importlib
import logging

from cerberus import Validator
from simple_settings import settings

from smedley.core import DriverConfig
from smedley.core.schemas import BASE_TASK_SCHEMA
from .exceptions import (
    InvalidTask,
    InvalidTaskLoaderClass,
    TaskDriverNotFound,
    TaskLoaderClassNotFound,
    TaskLoaderNotFound
)


logger = logging.getLogger(__name__)


class BaseTaskLoader:

    @classmethod
    def validate_loader(cls, loader):
        if not isinstance(loader, cls):
            raise InvalidTaskLoaderClass(loader=loader)

    @classmethod
    def validate_driver(cls, driver_name):
        if driver_name not in settings.DRIVERS:
            raise TaskDriverNotFound(driver_name=driver_name)

    @classmethod
    def get_loader(cls, loader_name):
        logger.info('Getting task loader {}'.format(loader_name))

        loader_class_path = settings.LOADERS.get(loader_name)
        if not loader_class_path:
            raise TaskLoaderNotFound(loader_name=loader_name)

        module_path, class_name = loader_class_path.rsplit('.', 1)
        try:
            module = importlib.import_module(module_path)
            _class = getattr(module, class_name)
        except:
            logger.exception(
                'Error on get loader {}'.format(loader_class_path)
            )
            raise TaskLoaderClassNotFound(loader_class_path=loader_class_path)

        loader = _class()
        cls.validate_loader(loader=loader)

        logger.info('Task loader {} initialized'.format(loader_name))

        return loader

    def get_driver(self, task):
        validator = Validator(BASE_TASK_SCHEMA, purge_unknown=True)
        if not validator.validate(task):
            raise InvalidTask(errors=validator.errors)

        data = validator.normalized(task)
        driver_name = data['driver']

        self.validate_driver(driver_name=driver_name)

        return driver_name

    def get_data(self, task, driver):
        config = DriverConfig(driver=driver)

        validator = Validator(config.get_task_schema(), purge_unknown=True)
        if not validator.validate(task):
            raise InvalidTask(errors=validator.errors)

        return validator.normalized(task)

    def _load_tasks(self):
        raise Exception('Load tasks not provided')

    def load_tasks(self):
        tasks = self._load_tasks()

        loaded_tasks = []
        for index, task in enumerate(tasks):
            logger.debug(
                'Loading task {}, raw task data {}'.format(index, task)
            )
            try:
                driver = self.get_driver(task=task)
                task_data = self.get_data(
                    task=task,
                    driver=driver
                )
                loaded_tasks.append(AttrDict(task_data))
            except:
                logger.exception('Fatal error on load task {}'.format(index))

        return loaded_tasks
