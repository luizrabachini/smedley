from .executors import SeleniumTaskExecutor
from .schemas import TASK_SCHEMA


class Config:

    schema = TASK_SCHEMA
    executor = SeleniumTaskExecutor
