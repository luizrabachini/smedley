class InvalidTaskLoaderClass(Exception):

    def __init__(self, loader):
        message = 'Class {} must be a subclass from BaseTaskLoader'.format(
            loader
        )
        super(InvalidTaskLoaderClass, self).__init__(message)


class InvalidTask(Exception):

    def __init__(self, errors):
        message = 'Invalid task found. Errors: {}'.format(errors)
        super(InvalidTask, self).__init__(message)


class TaskDriverNotFound(Exception):

    def __init__(self, driver_name):
        message = 'Driver {} not registered in settings'.format(driver_name)
        super(TaskDriverNotFound, self).__init__(message)


class TaskLoaderClassNotFound(Exception):

    def __init__(self, loader_class_path):
        message = 'Could not find loader class {}'.format(loader_class_path)
        super(TaskLoaderClassNotFound, self).__init__(message)


class TaskLoaderNotFound(Exception):

    def __init__(self, loader_name):
        message = (
            'A registered loader for name {} not found in settings'
        ).format(loader_name)
        super(TaskLoaderNotFound, self).__init__(message)
