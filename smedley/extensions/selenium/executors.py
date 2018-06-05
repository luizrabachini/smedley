import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from simple_settings import settings

from smedley.core.executors.base import BaseTaskExecutor
from smedley.core.validators.exceptions import ValidationError
from .constants import (
    FIREFOX,
    PHANTOMJS,
    CLICK,
    FILL
)
from .exceptions import BrowserNotFound
from .helpers import get_element
from .validators import (
    ElementValidator,
    SourceRegexValidator,
    UrlRegexValidator
)


logger = logging.getLogger(__name__)


class SeleniumTaskExecutor(BaseTaskExecutor):

    name = 'Selenium Task Executor'

    _validators = {
        'element': ElementValidator,
        'url_regex': SourceRegexValidator,
        'source_regex': UrlRegexValidator
    }

    _browser = None

    def _get_firefox_browser(self):
        logger.info('Loading Firefox Web Driver')

        options = FirefoxOptions()
        if settings.BROWSER_HEADLESS:
            options.add_argument('--headless')

        try:
            browser = Firefox(
                firefox_options=options,
                executable_path=settings.FIREFOX_GECKODRIVER_PATH
            )
        except Exception:
            logger.exception('Erro on load Firefox browser.')
            raise BrowserNotFound(browser=FIREFOX)

        logger.info('Firefox Web Driver loaded')

        return browser

    def _get_phantomjs_browser(self):
        logger.info('Loading PhantomJS Web Driver')

        try:
            browser = PhantomJS()
        except Exception:
            logger.exception('Erro on load PhantomJS browser.')
            raise BrowserNotFound(browser=PHANTOMJS)

        logger.info('PhantomJS Web Driver loaded')

        return browser

    def _apply_wait(self, step):
        wait = getattr(step, 'wait', None)
        if wait:
            time.sleep(wait)

        wait_for = getattr(step, 'wait_for', None)
        if wait_for:
            timeout = wait_for.timeout or settings.DEFAULT_DRIVER_WAIT
            locator = (
                getattr(By, wait_for.find_method.upper()),
                wait_for.find_value
            )
            WebDriverWait(self._browser, timeout).until(
                ec.presence_of_element_located(locator)
            )

    def _get_validator(self, validator_name):
        return self._validators[validator_name]()

    def _load(self, task):
        browser = task.browser

        if browser == FIREFOX:
            _browser = self._get_firefox_browser()
        elif browser == PHANTOMJS:
            _browser = self._get_phantomjs_browser()
        else:
            raise BrowserNotFound(browser=browser)

        window = getattr(task, 'window', None)
        if window:
            window_size = (window.width, window.height)
        else:
            window_size = settings.DEFAULT_WINDOW_SIZE

        _browser.set_window_size(*window_size)

        self._browser = _browser
        self._state = self._browser

        self._context['browser'] = _browser

    def _start_task(self, task):
        self._browser.get(task.url)

    def _finalize_task(self, task):
        self._browser.quit()

    def _execute_step(self, step):
        try:
            element = get_element(
                browser=self._browser,
                element=step.element
            )
        except NoSuchElementException:
            message = (
                'Element not found using find method {} and find value {}'
            ).format(step.element.find_method, step.element.find_value)
            raise ValidationError(message=message)

        if step.action == CLICK:
            element.click()
        elif step.action == FILL:
            element.send_keys(step.content)

        self._apply_wait(step=step)
