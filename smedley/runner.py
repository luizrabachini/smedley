import logging

from simple_settings import settings

from smedley.core.config import DriverConfig
from smedley.core.loaders import BaseTaskLoader


logger = logging.getLogger(__name__)


class Runner:

    def _execute(self, task):
        config = DriverConfig(driver=task.driver)
        executor = config.get_task_executor()
        executor.run(task=task)

    def _show_summary(self, tasks):
        message = 'Starting jobs to process {} tasks:\n'.format(len(tasks))
        for i, task in enumerate(tasks):
            message += '{} - {}\n'.format(i, task.name)
        logger.info(message)

    def _start(self, tasks):
        self._show_summary(tasks=tasks)
        for task in tasks:
            self._execute(task=task)

    def run(self):
        loader = BaseTaskLoader.get_loader(
            loader_name=settings.TASKS_LOADER
        )
        tasks = loader.load_tasks()
        self._start(tasks=tasks)
