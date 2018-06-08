import mock
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from simple_settings import settings

from smedley.core.validators.exceptions import ValidationError
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
        v1 = mock.Mock()
        v2 = mock.Mock()
        validators = {
            'v1': v1,
            'v2': v2
        }
        self.executor._validators = validators
        assert self.executor._get_validator(validator_name='v1') == v1
        assert self.executor._get_validator(validator_name='v2') == v2

    @mock.patch.object(SeleniumTaskExecutor, '_get_firefox_browser')
    def test__load_firefox(self, _get_firefox_browser, selenium_task):
        _get_firefox_browser.return_value = mock.MagicMock()
        self.executor._load(task=selenium_task)
        assert _get_firefox_browser.called

    @mock.patch.object(SeleniumTaskExecutor, '_get_phantomjs_browser')
    def test__load_phantomjs(self, _get_phantomjs_browser, selenium_task):
        selenium_task.browser = 'phantomjs'
        _get_phantomjs_browser.return_value = mock.MagicMock()
        self.executor._load(task=selenium_task)
        assert _get_phantomjs_browser.called

    @mock.patch.object(SeleniumTaskExecutor, '_get_firefox_browser')
    def test__load_default_window_size(
        self,
        _get_firefox_browser,
        selenium_task
    ):
        set_window_size = mock.MagicMock()
        browser = mock.MagicMock(set_window_size=set_window_size)
        _get_firefox_browser.return_value = browser
        self.executor._load(task=selenium_task)
        set_window_size.assert_called_with(1024, 768)
        assert self.executor._browser
        assert self.executor._state
        assert 'browser' in self.executor._context

    @mock.patch.object(SeleniumTaskExecutor, '_get_firefox_browser')
    def test__load_window_size(
        self,
        _get_firefox_browser,
        selenium_task
    ):
        selenium_task.update({
            'window': {
                'width': 2048,
                'height': 1024
            }
        })
        set_window_size = mock.MagicMock()
        browser = mock.MagicMock(set_window_size=set_window_size)
        _get_firefox_browser.return_value = browser
        self.executor._load(task=selenium_task)
        set_window_size.assert_called_with(2048, 1024)

    def test__start_task(self, selenium_task):
        browser_get = mock.MagicMock()
        browser = mock.MagicMock(get=browser_get)
        self.executor._browser = browser
        self.executor._start_task(task=selenium_task)
        browser_get.assert_called_with(selenium_task.url)

    def test__finalize_task(self, selenium_task):
        browser_quit = mock.MagicMock()
        browser = mock.MagicMock(quit=browser_quit)
        self.executor._browser = browser
        self.executor._finalize_task(task=selenium_task)
        assert browser_quit.quit

    @mock.patch('smedley.extensions.selenium.executors.get_element')
    @mock.patch.object(SeleniumTaskExecutor, '_apply_wait')
    @mock.patch.object(SeleniumTaskExecutor, '_apply_wait_for')
    def test__execute_step(
        self,
        _apply_wait_for,
        _apply_wait,
        get_element,
        step_click
    ):
        _apply_wait_for.return_value = None
        _apply_wait.return_value = None
        get_element.return_value = mock.Mock()
        self.executor._execute_step(step=step_click)
        assert _apply_wait_for.called
        assert _apply_wait.called
        assert get_element.called

    @mock.patch('smedley.extensions.selenium.executors.get_element')
    @mock.patch.object(SeleniumTaskExecutor, '_apply_wait')
    @mock.patch.object(SeleniumTaskExecutor, '_apply_wait_for')
    def test__execute_step_click(
        self,
        _apply_wait_for,
        _apply_wait,
        get_element,
        step_click
    ):
        _apply_wait_for.return_value = None
        _apply_wait.return_value = None
        click = mock.Mock()
        get_element.return_value = mock.Mock(click=click)
        self.executor._execute_step(step=step_click)
        assert click.called

    @mock.patch('smedley.extensions.selenium.executors.get_element')
    @mock.patch.object(SeleniumTaskExecutor, '_apply_wait')
    @mock.patch.object(SeleniumTaskExecutor, '_apply_wait_for')
    def test__execute_step_fill(
        self,
        _apply_wait_for,
        _apply_wait,
        get_element,
        step_fill
    ):
        _apply_wait_for.return_value = None
        _apply_wait.return_value = None
        send_keys = mock.Mock()
        get_element.return_value = mock.Mock(send_keys=send_keys)
        self.executor._execute_step(step=step_fill)
        send_keys.assert_called_with(step_fill.content)

    @mock.patch('smedley.extensions.selenium.executors.get_element')
    def test__execute_step_no_such_element(self, get_element, step_click):
        get_element.side_effect = NoSuchElementException()
        with pytest.raises(ValidationError):
            self.executor._execute_step(step=step_click)
