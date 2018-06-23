import mock
import pytest

from ..helpers import get_element


class TestHelpers:

    def test_get_element(self):
        find_element_by_test = mock.Mock()
        element = mock.Mock(find_method='test')
        browser = mock.Mock(find_element_by_test=find_element_by_test)
        get_element(browser, element)
        assert find_element_by_test.called

    def test_get_element_not_found(self):
        element = mock.Mock(find_method='test')
        with pytest.raises(AttributeError):
            get_element(object(), element)
