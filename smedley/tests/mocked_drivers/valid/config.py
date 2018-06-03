from smedley.core.executors.base import BaseTaskExecutor


class ValidExecutor(BaseTaskExecutor):

    pass


class Config:

    schema = {'name': str}
    executor = ValidExecutor
