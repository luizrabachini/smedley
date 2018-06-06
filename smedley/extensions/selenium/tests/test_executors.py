import mock
import pytest
from selenium.webdriver.common.by import By
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

        firefox_path = 'test/path/bin'
        settings.FIREFOX_EXECUTABLE_PATH = firefox_path
        settings.BROWSER_HEADLESS = True

        result = self.executor._get_firefox_browser()

        assert result == firefox_instance
        add_argument.assert_called_with('--headless')
        firefox.assert_called_with(
            firefox_options=options_instance,
            executable_path=firefox_path
        )

    def test__get_firefox_browser_not_found(self):
        settings.FIREFOX_EXECUTABLE_PATH = 'path/not/found/bin'

        with pytest.raises(BrowserNotFound):
            self.executor._get_firefox_browser()

    @mock.patch('smedley.extensions.selenium.executors.FirefoxOptions')
    @mock.patch('smedley.extensions.selenium.executors.Firefox')
    def test__get_firefox_browser_no_headless(self, firefox, options):
        add_argument = mock.Mock(return_value=None)
        options_instance = options.return_value
        options_instance.add_argument = add_argument

        firefox_path = 'test/path/bin'
        settings.FIREFOX_EXECUTABLE_PATH = firefox_path
        settings.BROWSER_HEADLESS = False

        self.executor._get_firefox_browser()

        assert not add_argument.called

    @mock.patch('smedley.extensions.selenium.executors.PhantomJS')
    def test__get_phantomjs_browser(self, phantomjs):
        phantomjs_instance = phantomjs.return_value

        phantomjs_path = 'test/path/bin'
        settings.PHANTOMJS_EXECUTABLE_PATH = phantomjs_path
        settings.BROWSER_HEADLESS = True

        result = self.executor._get_phantomjs_browser()

        assert result == phantomjs_instance
        phantomjs.assert_called_with(
            executable_path=phantomjs_path
        )

    def test__get_phantomjs_browser_not_found(self):
        settings.PHANTOMJS_EXECUTABLE_PATH = 'path/not/found/bin'

        with pytest.raises(BrowserNotFound):
            self.executor._get_phantomjs_browser()

    @mock.patch('smedley.extensions.selenium.executors.logger.warning')
    @mock.patch('smedley.extensions.selenium.executors.PhantomJS')
    def test__get_phantomjs_browser_no_headless(self, phantomjs, warning):
        phantomjs_path = 'test/path/bin'
        settings.PHANTOMJS_EXECUTABLE_PATH = phantomjs_path
        settings.BROWSER_HEADLESS = False

        self.executor._get_phantomjs_browser()

        assert warning.called

    @mock.patch('smedley.extensions.selenium.executors.time.sleep')
    def test__apply_wait(self, sleep, step_click):
        step_click.wait = 5
        step_click.wait_for = None

        self.executor._apply_wait(step=step_click)

        sleep.assert_called_with(step_click.wait)

    @mock.patch('smedley.extensions.selenium.executors.time.sleep')
    def test__apply_wait_not_required(self, sleep, step_click):
        step_click.wait = None
        step_click.wait_for = None

        self.executor._apply_wait(step=step_click)

        assert not sleep.called

    @mock.patch('smedley.extensions.selenium.executors.WebDriverWait')
    @mock.patch('smedley.extensions.selenium.executors.ec')
    def test__apply_wait_for(self, ec, web_driver, step_click):
        browser = mock.Mock()
        self.executor._browser = browser

        presence_result = None
        presence = mock.Mock(return_value=presence_result)
        ec.presence_of_element_located = presence

        until = mock.Mock(return_value=None)
        driver_wait = web_driver.return_value
        driver_wait.until = until

        locator = (By.CLASS_NAME, 'img-profile')

        self.executor._apply_wait_for(step=step_click)

        presence.assert_called_with(locator)
        until.assert_called_with(presence_result)
        web_driver.assert_called_with(browser, 3)

    @mock.patch('smedley.extensions.selenium.executors.WebDriverWait')
    def test__apply_wait_for_default_time(self, web_driver, step_click):
        browser = mock.Mock()
        self.executor._browser = browser

        settings.BROWSER_DEFAULT_WAIT = 20
        step_click['wait_for']['timeout'] = None

        self.executor._apply_wait_for(step=step_click)

        web_driver.assert_called_with(browser, 20)

    @mock.patch('smedley.extensions.selenium.executors.WebDriverWait.until')
    def test__apply_wait_for_not_required(self, until, step_click):
        step_click.wait_for = None

        self.executor._apply_wait_for(step=step_click)

        assert not until.called

    def test__get_validator(self):
        pass

    def test__load(self):
        pass

    def test__start_task(self):
        pass

    def test__finalize_task(self):
        pass

    def test__execute_step_click(self):
        pass

    def test__execute_step_fill(self):
        pass

    def test__execute_step_no_such_element(self):
        pass
