def get_element(browser, element):
    _find_method = getattr(
        browser,
        'find_element_by_{}'.format(element.find_method),
    )
    return _find_method(element.find_value)
