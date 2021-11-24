from pkg.command.azcli_cmd import AzCliCommand
from pkg.enums.Platform._platform import OSPlatform
from pkg._exception import FunctionAppPlanCreationException
from pkg.constant import Constant
from pkg.creator._creator import Creator
from pkg.entity._az_cli import AzCli
from pkg.enums.language._language import Language
from pkg.executor.azcli.command._azcli_cmd_executor import AzCliCommandExecutor
from pkg.utils import _name_creator


class FunctionPlanCreator(Creator):
    SKU_NAME = "EP1"

    def create(self, *args):
        lang: Language = args[0]
        platform: OSPlatform = args[1]
        az_cmd: AzCli = AzCli().append("functionapp").append("plan").append(Constant.CREATE). \
            append("--name").append(_name_creator.create_app_plan(lang, platform))\
            .append(Constant.ARG_LOCATION).append(Constant.REGION).append(Constant.ARG_RG).\
            append(Constant.RESOURCE_GROUP_NAME).append(Constant.ARG_SKU).append(self.SKU_NAME)

        if platform == OSPlatform.LINUX:
            az_cmd = az_cmd.append("--is-linux").append("true")
        try:
            az_cli_cmd: AzCliCommand = AzCliCommand(az_cmd)
            az_cli_cmd_executor = AzCliCommandExecutor(az_cli_cmd)
            res = az_cli_cmd_executor.execute()
        except Exception as e:
            raise FunctionAppPlanCreationException("Exception occured while creating app plan for language :: "+
                                                   lang.name.lower()+" for platform :: "+platform.name.lower()) from e

        return res