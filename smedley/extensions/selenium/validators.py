import re

from smedley.core.validators.base import BaseStepValidator
from smedley.core.validators.exceptions import ValidationError
from .helpers import get_element


class ElementValidator(BaseStepValidator):

    def _validate(self, context, data):
        browser = context['browser']
        element = get_element(browser=browser, element=data)
        if not element:
            raise ValidationError(
                'Element {} not found'.format(data.find_value)
            )


class SourceRegexValidator(BaseStepValidator):

    def _validate(self, context, data):
        browser = context['browser']
        regex = re.compile(data.pattern)
        result = re.search(regex, browser.page_source)
        if not result:
            raise ValidationError(
                'Regex {} not found in page source'.format(data.pattern)
            )


class UrlRegexValidator(BaseStepValidator):

    def _validate(self, context, data):
        browser = context['browser']
        regex = re.compile(data.pattern)
        result = re.search(regex, browser.current_url)
        if not result:
            raise ValidationError(
                'Current url {} not match regex {}'.format(
                    browser.current_url,
                    data.pattern
                )
            )
