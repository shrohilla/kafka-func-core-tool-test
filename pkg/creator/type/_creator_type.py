from enum import Enum


class CreatorType(Enum):
    STORAGE_ACCOUNT = 0
    FUNCTION_APP_PLAN = 1
    FUNCTION_APP = 2
    AZURE_RESOURCE = 3
    LOCAL_FUNCTION = 4