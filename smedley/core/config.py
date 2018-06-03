import importlib
import logging

from simple_settings import settings

from smedley.core.executors.base import BaseTaskExecutor
from .exceptions import (
    DriverConfigNotFound,
    DriverNotFound,
    InvalidDriverConfig
)


logger = logging.getLogger(__name__)


class DriverConfig:

    _configs = {}

    def __init__(self, driver):
        self._driver = driver
        self._load_config()

    def _load_config(self):
        if self._driver not in self._configs:
            config = self.get_config(driver=self._driver)
            self._configs[self._driver] = config

    @classmethod
    def validate_config(cls, config):
        required_attrs = ['schema', 'executor']
        for attr in required_attrs:
            attr_value = getattr(config, attr, None)
            if not attr_value:
                raise InvalidDriverConfig(
                    errors='Attr {} not found or empty'.format(attr)
                )

    @classmethod
    def validate_schema(cls, schema):
        if not isinstance(schema, dict):
            raise InvalidDriverConfig(
                errors='Schema must be a dict'
            )

    @classmethod
    def validate_executor(cls, executor):
        if not isinstance(executor, BaseTaskExecutor):
            raise InvalidDriverConfig(
                errors='Executor must be a subclass of BaseTaskExecutor'
            )

    @classmethod
    def get_config(cls, driver):
        logger.info('Getting config of driver {}'.format(driver))

        driver_path = settings.DRIVERS.get(driver)
        if not driver_path:
            raise DriverNotFound(driver=driver)

        module_path = '{}.config'.format(driver_path)
        try:
            module = importlib.import_module(module_path)
            _class = getattr(module, 'Config')
        except:
            logger.exception(
                'Error on get config {}'.format(module_path)
            )
            raise DriverConfigNotFound(driver=driver)

        config = _class()
        cls.validate_config(config=config)

        logger.info('Config of driver {} initialized'.format(driver))

        return config

    def get_task_schema(self):
        schema = self._configs[self._driver].schema
        self.validate_schema(schema=schema)
        return schema

    def get_task_executor(self):
        _class = self._configs[self._driver].executor
        executor = _class()
        self.validate_executor(executor=executor)
        return executor
