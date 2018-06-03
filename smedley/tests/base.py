from simple_settings import settings


class BaseTest:

    def setup(self):
        settings.DRIVERS = {
            'test': 'smedley.tests.mocked_drivers.valid'
        }
