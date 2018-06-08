from attrdict import AttrDict

import pytest


@pytest.fixture
def step_click():
    return AttrDict({
        'name': 'Click in About',
        'element': {
            'find_method': 'xpath',
            'find_value': '//*[@id="footer"]/div/div/div/div/a[2]'
        },
        'action': 'click',
        'wait_for': {
            'find_method': 'class_name',
            'find_value': 'img-profile',
            'timeout': 3
        }
    })


@pytest.fixture
def step_fill():
    return AttrDict({
        'name': 'Click in About',
        'element': {
            'find_method': 'xpath',
            'find_value': '//*[@id="footer"]/div/div/div/div/a[2]'
        },
        'action': 'fill',
        'content': 'test'
    })


@pytest.fixture
def selenium_task(step_click, step_fill):
    return AttrDict({
        'name': 'Test Personal Page',
        'url': 'http://luizrabachini.com',
        'browser': 'firefox',
        'steps': [
            step_click,
            step_fill
        ]
    })
