from decouple import config, Csv


LOADERS = {
    'file': 'smedley.core.loaders.FileTaskLoader',
    'server': 'smedley.core.loaders.ServerTaskLoader'
}

DRIVERS = {
    'selenium': 'smedley.extensions.selenium'
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s %(asctime)s '
                '%(module)s %(process)d %(thread)d %(message)s'
            )
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'logconsole': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': config('LOG_FILE'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,  # 50 MB total
            'formatter': 'verbose',
        },
        'logentries': {
            'level': 'INFO',
            'class': 'logentries.LogentriesHandler',
            'token': config('LOGENTRIES_TOKEN'),
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'smedley': {
            'handlers': config(
                'LOG_HANDLERS',
                cast=Csv(),
                default='logconsole'
            ),
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

TASKS_LOADER = config('TASKS_LOADER')
TASKS_FILE_PATH = config('TASKS_FILE_PATH')
TASKS_MASTER_SERVER = config('TASKS_MASTER_SERVER')
TASKS_MASTER_SERVER_TIMEOUT = config('TASKS_MASTER_SERVER_TIMEOUT', cast=int)


# Extensions / Selenium

BROWSER_HEADLESS = config('BROWSER_HEADLESS', cast=bool, default=True)

BROWSER_WINDOW_SIZE = (1024, 768)  # pixels
BROWSER_DRIVER_WAIT = 5  # seconds

FIREFOX_GECKODRIVER_PATH = config('FIREFOX_GECKODRIVER_PATH')
