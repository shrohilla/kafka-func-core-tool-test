from pkg.enums.Platform._platform import OSPlatform
from pkg._exception import FunctionAppPlanCreationException
from pkg.constant import Constant
from pkg.creator._creator import Creator
from pkg.entity._az_cli import AzCli
from pkg.executor.azcli._az_cli_executor import AzCliExecutor
from pkg.enums.language._language import Language
from pkg.utils import _name_creator


class FunctionPlanCreator(Creator):
    SKU_NAME = "EP1"

    def __init__(self):
        self._az_cli_executor = AzCliExecutor()

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
            res = self._az_cli_executor.run_az_cli(az_cmd)
        except Exception as e:
            raise FunctionAppPlanCreationException("Exception occured while creating app plan for language :: "+
                                                   lang.name.lower()+" for platform :: "+platform.name.lower()) from e

        return res