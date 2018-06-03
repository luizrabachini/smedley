import mock
import pytest

from smedley.core.validators.exceptions import ValidationError
from ..base import BaseTaskExecutor


class TestBaseTaskExecutor:

    def setup(self):
        self.executor = BaseTaskExecutor()

    def test__init(self):
        assert self.executor._context == {}

    def test__load(self, task):
        with pytest.raises(Exception):
            self.executor._load(task=task)

    @mock.patch.object(BaseTaskExecutor, '_load')
    def test_load(self, _load, task):
        _load.return_value = None
        self.executor.load(task=task)
        assert _load.called

    def test__start_task(self, task):
        with pytest.raises(Exception):
            self.executor._start_task(task=task)

    @mock.patch.object(BaseTaskExecutor, '_start_task')
    def test_start_task(self, _start_task, task):
        _start_task.return_value = None
        self.executor.start_task(task=task)
        assert _start_task.called

    def test__finalize_task(self, task):
        with pytest.raises(Exception):
            self.executor._finalize_task(task=task)

    @mock.patch.object(BaseTaskExecutor, '_finalize_task')
    def test_finalize_task(self, _finalize_task, task):
        _finalize_task.return_value = None
        self.executor.finalize_task(task=task)
        assert _finalize_task.called

    def test__execute_step(self, step):
        with pytest.raises(Exception):
            self.executor._execute_step(step=step)

    @mock.patch.object(BaseTaskExecutor, '_execute_step')
    def test_execute_step(self, _execute_step, step):
        _execute_step.return_value = None
        self.executor.execute_step(step=step)
        assert _execute_step.called

    def test__get_validator(self):
        with pytest.raises(Exception):
            self.executor._get_validator(validator_name='test')

    @mock.patch.object(BaseTaskExecutor, '_get_validator')
    def test_get_validator(self, _get_validator, step):
        _get_validator.return_value = None
        self.executor.get_validator(validator_name='test')
        assert _get_validator.called

    @mock.patch.object(BaseTaskExecutor, 'get_validator')
    def test_validate_step(self, get_validator, step):
        validate = mock.Mock()
        validator = mock.Mock(validate=validate)
        get_validator.return_value = validator
        step.validators = [{'content': None}]
        self.executor.validate_step(step=step)
        get_validator.assert_called_with(validator_name='content')
        validate.assert_called_with(context={}, data=None)

    @mock.patch.object(BaseTaskExecutor, 'get_validator')
    def test_validate_step_list(self, get_validator, step):
        validate = mock.Mock()
        validator = mock.Mock(validate=validate)
        get_validator.return_value = validator
        step.validators = [{'content': None}, {'url': None}]
        self.executor.validate_step(step=step)
        assert get_validator.call_count == 2
        assert validate.call_count == 2

    @mock.patch.object(BaseTaskExecutor, 'load')
    @mock.patch.object(BaseTaskExecutor, 'start_task')
    @mock.patch.object(BaseTaskExecutor, 'execute_step')
    @mock.patch.object(BaseTaskExecutor, 'validate_step')
    @mock.patch.object(BaseTaskExecutor, 'finalize_task')
    def test_run(
        self,
        finalize_task,
        validate_step,
        execute_step,
        start_task,
        load,
        task,
        steps
    ):
        finalize_task.return_value = None
        validate_step.return_value = None
        execute_step.return_value = None
        start_task.return_value = None
        load.return_value = None
        task.steps = steps
        self.executor.run(task=task)
        assert finalize_task.call_count == 1
        assert validate_step.call_count == 3
        assert execute_step.call_count == 3
        assert start_task.call_count == 1
        assert load.call_count == 1

    @mock.patch.object(BaseTaskExecutor, 'load')
    @mock.patch.object(BaseTaskExecutor, 'start_task')
    @mock.patch.object(BaseTaskExecutor, 'execute_step')
    @mock.patch.object(BaseTaskExecutor, 'validate_step')
    @mock.patch.object(BaseTaskExecutor, 'finalize_task')
    def test_run_step_required(
        self,
        finalize_task,
        validate_step,
        execute_step,
        start_task,
        load,
        task,
        steps
    ):
        finalize_task.return_value = None
        validate_step.side_effect = [
            None,
            ValidationError('Error')
        ]
        execute_step.return_value = None
        start_task.return_value = None
        load.return_value = None
        task.steps = steps
        self.executor.run(task=task)
        assert finalize_task.call_count == 1
        assert validate_step.call_count == 2
        assert execute_step.call_count == 2
        assert start_task.call_count == 1
        assert load.call_count == 1

    @mock.patch.object(BaseTaskExecutor, 'load')
    @mock.patch.object(BaseTaskExecutor, 'start_task')
    @mock.patch.object(BaseTaskExecutor, 'execute_step')
    @mock.patch.object(BaseTaskExecutor, 'validate_step')
    @mock.patch.object(BaseTaskExecutor, 'finalize_task')
    def test_run_step_not_required(
        self,
        finalize_task,
        validate_step,
        execute_step,
        start_task,
        load,
        task,
        steps
    ):
        finalize_task.return_value = None
        validate_step.side_effect = [
            None,
            ValidationError('Error')
        ]
        execute_step.return_value = None
        start_task.return_value = None
        load.return_value = None
        steps[1].required = False
        task.steps = steps
        self.executor.run(task=task)
        assert finalize_task.call_count == 1
        assert validate_step.call_count == 3
        assert execute_step.call_count == 3
        assert start_task.call_count == 1
        assert load.call_count == 1
