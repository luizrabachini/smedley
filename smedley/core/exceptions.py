class DriverConfigNotFound(Exception):

    def __init__(self, driver):
        message = 'Config not found for driver {}'.format(driver)
        super(DriverConfigNotFound, self).__init__(message)


class DriverNotFound(Exception):

    def __init__(self, driver):
        message = 'Driver {} not found'.format(driver)
        super(DriverNotFound, self).__init__(message)


class InvalidDriverConfig(Exception):

    def __init__(self, errors):
        message = 'Invalid config found, errors {}'.format(errors)
        super(InvalidDriverConfig, self).__init__(message)
