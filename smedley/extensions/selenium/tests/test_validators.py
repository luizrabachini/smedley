import mock
import pytest

from smedley.core.validators.exceptions import ValidationError
from ..validators import (
    ElementValidator,
    SourceRegexValidator,
    UrlRegexValidator
)


class BaseTestValidator:

    def setup(self):
        self.browser = mock.Mock()
        self.context = {'browser': self.browser}


class TestElementValidator(BaseTestValidator):

    def test__validate(self):
        data = mock.Mock(find_method='test')
        self.browser.get_element_by_test = mock.Mock()
        assert not ElementValidator()._validate(
            context=self.context,
            data=data
        )

    @mock.patch('smedley.extensions.selenium.validators.get_element')
    def test__validate_error(self, get_element):
        get_element.return_value = None
        data = mock.Mock(find_method='test')
        self.browser.get_element_by_test = mock.Mock()
        with pytest.raises(ValidationError):
            ElementValidator()._validate(
                context=self.context,
                data=data
            )


class TestSourceRegexValidator(BaseTestValidator):

    def test__validate(self):
        data = mock.Mock(pattern='.*<p>XPTO.*')
        self.browser.page_source = '<html>Test <p>XPTO</p></html>'
        assert not SourceRegexValidator()._validate(
            context=self.context,
            data=data
        )

    def test__validate_error(self):
        data = mock.Mock(pattern='.*<p>XPTO.*')
        self.browser.page_source = '<html>Test <p>123XPTO</p></html>'
        with pytest.raises(ValidationError):
            SourceRegexValidator()._validate(
                context=self.context,
                data=data
            )


class TestUrlRegexValidator(BaseTestValidator):

    def test__validate(self):
        data = mock.Mock(pattern='http://.*/test.*')
        self.browser.current_url = 'http://test.com/test?next=2'
        assert not UrlRegexValidator()._validate(
            context=self.context,
            data=data
        )

    def test__validate_error(self):
        data = mock.Mock(pattern='http://.*/test.*')
        self.browser.current_url = 'https://test.com/test?next=2'
        with pytest.raises(ValidationError):
            UrlRegexValidator()._validate(
                context=self.context,
                data=data
            )
