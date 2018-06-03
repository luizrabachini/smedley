from smedley.core.schemas import BASE_STEP_SCHEMA, BASE_TASK_SCHEMA

from .constants import ACTIONS, BROWSERS


ELEMENT_SCHEMA = {
    'find_method': {
        'type': 'string',
        'allowed': [
            'id',
            'name',
            'xpath',
            'link_text',
            'partial_link_text',
            'tag_name',
            'class_name',
            'css_selector'
        ],
        'required': True,
        'empty': False
    },
    'find_value': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}


REGEX_SCHEMA = {
    'pattern': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}


VALIDATOR_SCHEMA = {
    'element': {
        'type': 'dict',
        'schema': ELEMENT_SCHEMA,
        'required': False
    },
    'url_regex': {
        'type': 'dict',
        'schema': REGEX_SCHEMA,
        'required': False
    },
    'source_regex': {
        'type': 'dict',
        'schema': REGEX_SCHEMA,
        'required': False
    }
}


WAIT_FOR_SCHEMA = dict(
    ELEMENT_SCHEMA,
    **{
        'timeout': {
            'type': 'integer',
            'required': False,
            'default': 0,
            'min': 0
        }
    }
)


STEP_SCHEMA = dict(
    BASE_STEP_SCHEMA,
    **{
        'element': {
            'type': 'dict',
            'schema': ELEMENT_SCHEMA,
            'required': True
        },
        'action': {
            'type': 'string',
            'allowed': ACTIONS,
            'required': True,
            'empty': False
        },
        'content': {
            'type': 'string',
            'required': False,
            'default': ''
        },
        'wait': {
            'type': 'integer',
            'required': False,
            'default': 0,
            'min': 0
        },
        'wait_for': {
            'type': 'dict',
            'schema': WAIT_FOR_SCHEMA,
            'required': False
        }
    }
)
STEP_SCHEMA['validators']['schema'] = {
    'type': 'dict',
    'schema': VALIDATOR_SCHEMA
}


WINDOW_SCHEMA = {
    'width': {
        'type': 'integer',
        'required': True,
        'min': 0
    },
    'height': {
        'type': 'integer',
        'required': True,
        'min': 0
    }
}


TASK_SCHEMA = dict(
    BASE_TASK_SCHEMA,
    **{
        'url': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'window': {
            'type': 'dict',
            'schema': WINDOW_SCHEMA,
            'required': False
        },
        'browser': {
            'type': 'string',
            'allowed': BROWSERS,
            'required': True,
            'empty': False
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
