import mock
import pytest

from .conftest import ValidStepValidator
from ..base import BaseStepValidator
from ..exceptions import InvalidStepValidatorClass


class TestBaseStepValidator:

    def setup(self):
        self.validator = BaseStepValidator()

    def test_validate_validator(self):
        BaseStepValidator.validate_validator(validator=ValidStepValidator())

    def test_validate_validator_error(self):
        with pytest.raises(InvalidStepValidatorClass):
            BaseStepValidator.validate_validator(validator=object())

    def test__validate(self):
        with pytest.raises(Exception):
            self.validator._validate(None, None)

    @mock.patch.object(BaseStepValidator, '_validate')
    def test_validate(self, _validate):
        _validate.return_value = None
        self.validator.validate(None, None)
        assert _validate.called
