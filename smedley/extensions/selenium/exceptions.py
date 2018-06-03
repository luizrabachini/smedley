class BrowserNotFound(Exception):

    def __init__(self, browser):
        message = 'Browser {} not found'.format(browser)
        super(BrowserNotFound, self).__init__(message)
