from simple_settings import settings

from smedley.core.schemas import BASE_STEP_SCHEMA, BASE_TASK_SCHEMA

from .constants import ACTIONS


VALIDATOR_SCHEMA = {
    'response_time': {
        'type': 'integer',
        'required': False
    },
    'http_status_code': {
        'type': 'integer',
        'required': False
    },
    'http_headers': {
        'type': 'dict',
        'required': False
    },
    'body_json_attr': {
        'type': 'dict',
        'required': False
    }
}


STEP_SCHEMA = dict(
    BASE_STEP_SCHEMA,
    **{
        'action': {
            'type': 'string',
            'allowed': ACTIONS,
            'required': True,
            'empty': False
        },
        'data': {
            'type': 'string',
            'required': False,
            'empty': False
        },
        'payload': {
            'type': 'dict',
            'required': False,
            'empty': False
        },
        'headers': {
            'type': 'dict',
            'required': False
        },
        'params': {
            'type': 'dict',
            'required': False
        },
        'timeout': {
            'type': 'integer',
            'required': False,
            'default': settings.DEFAULT_REQUESTS_TIMEOUT,
            'min': 0
        }
    }
)
STEP_SCHEMA['validators']['schema'] = {
    'type': 'dict',
    'schema': VALIDATOR_SCHEMA
}


TASK_SCHEMA = dict(
    BASE_TASK_SCHEMA,
    **{
        'url': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'session': {
            'type': 'boolean',
            'required': False,
            'default': False
        },
        'steps': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': STEP_SCHEMA
            },
            'required': True
        }
    }
)
