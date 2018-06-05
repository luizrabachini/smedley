import mock
import pytest
from simple_settings import settings

from ..executors import SeleniumTaskExecutor
from ..exceptions import BrowserNotFound


class TestSeleniumTaskExecutor:

    def setup(self):
        self.executor = SeleniumTaskExecutor()

    @mock.patch('smedley.extensions.selenium.executors.FirefoxOptions')
    @mock.patch('smedley.extensions.selenium.executors.Firefox')
    def test__get_firefox_browser(self, firefox, options):
        add_argument = mock.Mock(return_value=None)
        options_instance = options.return_value
        options_instance.add_argument = add_argument

        firefox_instance = firefox.return_value

        firefox_bin_path = 'test/path/bin'
        settings.FIREFOX_GECKODRIVER_PATH = firefox_bin_path
        settings.BROWSER_HEADLESS = True

        result = self.executor._get_firefox_browser()

        assert result == firefox_instance
        add_argument.assert_called_with('--headless')
        firefox.assert_called_with(
            firefox_options=options_instance,
            executable_path=firefox_bin_path
        )

    def test__get_firefox_browser_not_found(self):
        settings.FIREFOX_GECKODRIVER_PATH = 'path/not/found/bin'

        with pytest.raises(BrowserNotFound):
            self.executor._get_firefox_browser()

    @mock.patch('smedley.extensions.selenium.executors.FirefoxOptions')
    @mock.patch('smedley.extensions.selenium.executors.Firefox')
    def test__get_firefox_browser_no_headless(self, firefox, options):
        add_argument = mock.Mock(return_value=None)
        options_instance = options.return_value
        options_instance.add_argument = add_argument

        firefox_bin_path = 'test/path/bin'
        settings.FIREFOX_GECKODRIVER_PATH = firefox_bin_path
        settings.BROWSER_HEADLESS = False

        self.executor._get_firefox_browser()

        assert not add_argument.called

    def test__get_phantomjs_browser(self):
        assert False

    def test__get_phantomjs_browser_not_found(self):
        assert False

    def test__apply_wait(self):
        assert False

    def test__apply_wait_not_required(self):
        assert False

    def test__apply_wait_for(self):
        assert False

    def test__apply_wait_for_not_required(self):
        assert False

    def test__get_validator(self):
        assert False

    def test__load(self):
        assert False

    def test__start_task(self):
        assert False

    def test__finalize_task(self):
        assert False

    def test__execute_step_click(self):
        assert False

    def test__execute_step_fill(self):
        assert False

    def test__execute_step_no_such_element(self):
        assert False
