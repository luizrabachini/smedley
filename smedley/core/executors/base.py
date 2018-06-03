import logging

from smedley.core.validators.exceptions import ValidationError


logger = logging.getLogger(__name__)


class BaseTaskExecutor:

    name = 'Base Task Executor'

    _context = None

    def __init__(self):
        self._context = {}

    def _load(self, task):
        raise Exception('Load task not provided')

    def load(self, task):
        logger.info('Loading executor {}'.format(self.name))
        return self._load(task=task)

    def _start_task(self, task):
        raise Exception('Start task not provided')

    def start_task(self, task):
        logger.info('Starting task {}'.format(task.name))
        return self._start_task(task=task)

    def _finalize_task(self, task):
        raise Exception('Finalize task not provided')

    def finalize_task(self, task):
        logger.info('Finalizing task {}'.format(task.name))
        return self._finalize_task(task=task)

    def _execute_step(self, step):
        raise Exception('Execute step not provided')

    def execute_step(self, step):
        logger.info('Executing step {}'.format(step.name))
        return self._execute_step(step=step)

    def _get_validator(self, validator_name):
        raise Exception('Get validator not provided')

    def get_validator(self, validator_name):
        logger.info('Getting validator {}'.format(validator_name))
        return self._get_validator(validator_name=validator_name)

    def validate_step(self, step):
        for step_validator in step.validators:
            for validator_name in step_validator.keys():
                validator = self.get_validator(
                    validator_name=validator_name
                )
                validator.validate(
                    context=self._context,
                    data=getattr(step_validator, validator_name)
                )

    def run(self, task):
        self.load(task=task)
        self.start_task(task=task)

        for step in task.steps:
            step_id = 'Task {}; Step {}'.format(task.name, step.name)
            step_error = True

            try:
                self.execute_step(step=step)
                self.validate_step(step=step)
            except ValidationError as e:
                logger.error(
                    '{}; Validation Error {}'.format(step_id, e)
                )
            except Exception:
                logger.exception('{} Fatal Error'.format(step_id))
            else:
                step_error = False

            if step_error:
                if step.required:
                    logger.error(
                        '{}; Step required, stop test'.format(step_id)
                    )
                    break
                else:
                    logger.error(
                        '{}; Step not required, continue test'.format(step_id)
                    )

        self.finalize_task(task=task)
