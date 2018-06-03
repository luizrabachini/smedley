import mock
import pytest
from simple_settings import settings

from smedley.core import DriverConfig
from smedley.core.exceptions import (
    DriverConfigNotFound,
    DriverNotFound,
    InvalidDriverConfig
)
from smedley.tests.mocked_drivers.valid.config import (
    Config,
    ValidExecutor
)


class TestDriverConfig:

    def setup(self):
        DriverConfig._configs = {}

    @mock.patch.object(DriverConfig, '_load_config')
    def test_init(self, _load_config):
        _load_config.return_value = None
        config = DriverConfig(driver='test')
        assert config._driver == 'test'
        assert _load_config.called

    @mock.patch.object(DriverConfig, 'get_config')
    def test__load_config(self, get_config):
        get_config.return_value = None
        config = DriverConfig(driver='test')
        assert config
        assert get_config.called

    @mock.patch.object(DriverConfig, 'get_config')
    def test__load_config_previous_initialized(self, get_config):
        get_config.return_value = None
        config1 = DriverConfig(driver='test')
        assert config1
        config2 = DriverConfig(driver='test')
        assert config2
        assert get_config.call_count == 1

    def test_validate_config(self, valid_config):
        result = DriverConfig.validate_config(config=valid_config)
        assert result is None

    @pytest.mark.parametrize('field', ['schema', 'executor'])
    def test_validate_config_error(self, field, valid_config):
        setattr(valid_config, field, None)
        with pytest.raises(InvalidDriverConfig):
            DriverConfig.validate_config(config=valid_config)

    def test_validate_schema(self, valid_schema):
        result = DriverConfig.validate_schema(schema=valid_schema)
        assert result is None

    def test_validate_schema_error(self):
        with pytest.raises(InvalidDriverConfig):
            DriverConfig.validate_schema(schema=None)

    def test_validate_executor(self, valid_executor):
        result = DriverConfig.validate_executor(executor=valid_executor)
        assert result is None

    def test_validate_executor_error(self):
        with pytest.raises(InvalidDriverConfig):
            DriverConfig.validate_executor(executor=object())

    @mock.patch.object(DriverConfig, 'validate_config')
    def test_get_config(self, validate_config):
        validate_config.return_value = None
        driver_name = 'valid'
        settings.DRIVERS = {
            driver_name: 'smedley.tests.mocked_drivers.valid'
        }
        config = DriverConfig.get_config(driver=driver_name)
        assert isinstance(config, Config)
        assert validate_config.called

    def test_get_config_driver_not_found(self):
        settings.DRIVERS = {
            'some_driver': 'some.path'
        }
        with pytest.raises(DriverNotFound):
            DriverConfig.get_config(driver='potato')

    def test_get_config_not_found(self):
        driver_name = 'no_config'
        settings.DRIVERS = {
            driver_name: 'smedley.tests.mocked_drivers.no_config'
        }
        with pytest.raises(DriverConfigNotFound):
            DriverConfig.get_config(driver=driver_name)

    def test_get_task_schema(self):
        driver_name = 'valid'
        settings.DRIVERS = {
            driver_name: 'smedley.tests.mocked_drivers.valid'
        }
        config = DriverConfig(driver=driver_name)
        assert config.get_task_schema() == Config.schema

    def test_get_task_executor(self):
        driver_name = 'valid'
        settings.DRIVERS = {
            driver_name: 'smedley.tests.mocked_drivers.valid'
        }
        config = DriverConfig(driver=driver_name)
        executor = config.get_task_executor()
        assert isinstance(executor, ValidExecutor)
