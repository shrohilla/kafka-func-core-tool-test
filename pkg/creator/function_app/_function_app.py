from pkg.enums.Platform._platform import OSPlatform
from pkg._exception import FunctionAppAzureCreationException
from pkg.constant import Constant
from pkg.creator._creator import Creator
from pkg.entity._az_cli import AzCli
from pkg.executor.azcli._az_cli_executor import AzCliExecutor
from pkg.enums.language._language import Language
from pkg.utils import _name_creator


class FunctionAppCreator(Creator):
    SKU_NAME = "EP1"

    def __init__(self):
        self._az_cli_executor = AzCliExecutor()

    def create(self, *args):
        lang: Language = args[0]
        platform: OSPlatform = args[1]
        run_time = lang.name.lower()
        if Language.JAVASCRIPT == lang or Language.TYPESCRIPT == lang:
            run_time = 'node'
        az_cmd = self._create_azcli_cmd(lang, platform, run_time)
        try:
            res = self._az_cli_executor.run_az_cli(az_cmd)
        except Exception as e:
            raise FunctionAppAzureCreationException("Exception occured while creating function app for language :: " +
                                                   lang.name.lower() + " for platform :: " + platform.name.lower()) from e

        return res

    def _create_azcli_cmd(self, lang, platform, run_time):
        az_cli_cmd = AzCli().append("functionapp").append(Constant.CREATE). \
            append("--name").append(_name_creator.create_function_app(lang, platform)).\
            append("--storage-account").append(_name_creator.create_storage_account(lang)).append("--plan"). \
            append(_name_creator.create_app_plan(lang, platform)).append(Constant.ARG_RG). \
            append(Constant.RESOURCE_GROUP_NAME).append("--runtime").append(run_time). \
            append("--functions-version").append(Constant.FUNCTION_VERSION)
        if Language.JAVASCRIPT == lang:
            az_cli_cmd.append("--runtime-version").append('10')
        return az_cli_cmd
