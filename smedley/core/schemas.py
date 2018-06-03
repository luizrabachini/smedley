BASE_TASK_SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'driver': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'steps': {
        'type': 'list',
        'required': True
    }
}


BASE_STEP_SCHEMA = {
    'name': {
        'type': 'string',
        'required': False,
        'empty': False,
        'default': 'NONAME'
    },
    'required': {
        'type': 'boolean',
        'required': False,
        'default': True
    },
    'validators': {
        'type': 'list',
        'required': False,
        'default': []
    }
}
