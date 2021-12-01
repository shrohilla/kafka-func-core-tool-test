from pkg.command.azcli_cmd import AzCliCommand
from pkg.enums.Platform._platform import OSPlatform
from pkg._exception import FunctionAppAzureCreationException
from pkg.constant import Constant
from pkg.creator._creator import Creator
from pkg.entity._az_cli import AzCli
from pkg.enums.language._language import Language
from pkg.executor.azcli.command._azcli_cmd_executor import AzCliCommandExecutor
from pkg.utils import _name_creator


class FunctionAppCreator(Creator):
    SKU_NAME = "EP1"

    def create(self, *args):
        lang: Language = args[0]
        platform: OSPlatform = args[1]
        run_time = lang.name.lower()
        # TODO
        if Language.TYPESCRIPT == lang or Language.JAVASCRIPT == lang :
            run_time = 'node'
        az_cmd = self._create_azcli_cmd(lang, platform, run_time)
        try:
            az_cli_cmd: AzCliCommand = AzCliCommand(az_cmd)
            az_cli_cmd_executor = AzCliCommandExecutor(az_cli_cmd)
            res = az_cli_cmd_executor.execute()
        except Exception as e:
            raise FunctionAppAzureCreationException("Exception occured while creating function app for language :: " +
                                                   lang.name.lower() + " for platform :: " + platform.name.lower()) from e

        return res

    def _create_azcli_cmd(self, lang, platform, run_time):
        az_cli_cmd = AzCli().append(Constant.FUNCTION_APP).append(Constant.CREATE). \
            append("--name").append(_name_creator.create_function_app(lang, platform)).\
            append("--storage-account").append(_name_creator.create_storage_account(lang)).append("--plan"). \
            append(_name_creator.create_app_plan(lang, platform)).append(Constant.ARG_RG). \
            append(Constant.RESOURCE_GROUP_NAME).append("--runtime").append(run_time). \
            append("--functions-version").append(Constant.FUNCTION_VERSION)
        #TODO
        if Language.TYPESCRIPT == lang or Language.JAVASCRIPT == lang:
            az_cli_cmd.append("--runtime-version").append('14')
        return az_cli_cmd
