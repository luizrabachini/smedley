from attrdict import AttrDict

import pytest


@pytest.fixture
def task():
    return AttrDict({
        'name': 'Test',
        'driver': 'test',
        'steps': []
    })


@pytest.fixture
def tasks():
    return [
        task(),
        task()
    ]


@pytest.fixture
def step():
    return AttrDict({
        'name': 'Step Test',
        'required': True,
        'validators': []
    })


@pytest.fixture
def steps():
    return [
        step(),
        step(),
        step()
    ]


@pytest.fixture
def step_not_required(step):
    step.required = False
    return step
