from pkg.constant import Constant
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.language._language import Language

_test = "test"


def create_function_app(lang: Language, platform: OSPlatform):
    fn_app_name = "kafkaext" + lang.name.lower() + "-" + platform.name.lower() + _test
    if len(fn_app_name) > 24:
        fn_app_name = fn_app_name[0:23]
    return fn_app_name


def create_storage_account(lang: Language):
    storage_account_name = Constant.STORAGE_ACCOUNT_NAME + lang.name.lower() + _test
    if len(storage_account_name) > 24:
        storage_account_name = storage_account_name[0:23]
    return storage_account_name


def create_app_plan(lang: Language, platform: OSPlatform):
    return Constant.APP_PLAN_NAME + lang.name.lower() + "-" + platform.name.lower() + _test
