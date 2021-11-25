class FilePathNotFoundInArgs(Exception):
    pass


class StorageAccountCreationException(Exception):
    pass


class FunctionAppPlanCreationException(Exception):
    pass


class NoMessageFoundException(Exception):
    pass


class FunctionAppAzureCreationException(Exception):
    pass


class ValidationFailedException(Exception):
    pass


class EventHubDataNotProcessedException(Exception):
    pass


class TestFailedException(Exception):
    pass
