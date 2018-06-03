class InvalidStepValidatorClass(Exception):

    def __init__(self, validator):
        message = 'Class {} must be a subclass from BaseStepValidator'.format(
            validator
        )
        super(InvalidStepValidatorClass, self).__init__(message)


class ValidationError(Exception):

    def __init__(self, message):
        super(ValidationError, self).__init__(message)
