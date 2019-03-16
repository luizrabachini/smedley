from .executors import RequestsTaskExecutor
from .schemas import TASK_SCHEMA


class Config:

    schema = TASK_SCHEMA
    executor = RequestsTaskExecutor
