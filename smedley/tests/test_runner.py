import mock

from .base import BaseTest
from ..runner import Runner


class TestRunner(BaseTest):

    @mock.patch('smedley.core.config.DriverConfig.get_task_executor')
    def test__execute(self, get_task_executor, tasks):
        runner = Runner()
        run = mock.Mock(return_value=None)
        executor = mock.Mock(run=run)
        get_task_executor.return_value = executor
        runner._execute(task=tasks[0])
        assert run.called

    @mock.patch('smedley.runner.logger.info')
    def test__show_summary(self, info, tasks):
        runner = Runner()
        runner._show_summary(tasks=tasks)
        assert info.called

    @mock.patch.object(Runner, '_execute')
    @mock.patch.object(Runner, '_show_summary')
    def test__start(self, _show_summary, _execute, tasks):
        runner = Runner()
        runner._start(tasks=tasks)
        assert _show_summary.called
        assert _execute.call_count == len(tasks)

    @mock.patch('smedley.core.loaders.BaseTaskLoader.get_loader')
    @mock.patch.object(Runner, '_start')
    def test_run(self, _start, get_loader, tasks):
        runner = Runner()
        _start.return_value = None
        load_tasks = mock.Mock(return_value=tasks)
        get_loader.return_value = mock.Mock(load_tasks=load_tasks)
        runner.run()
        assert _start.called
