from .exceptions import InvalidStepValidatorClass


class BaseStepValidator:

    @classmethod
    def validate_validator(cls, validator):
        if not isinstance(validator, cls):
            raise InvalidStepValidatorClass(validator=validator)

    def _validate(self, context, data):
        raise Exception('Validate method not provided')

    def validate(self, context, data):
        return self._validate(context=context, data=data)
