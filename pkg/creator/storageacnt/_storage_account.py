from pkg._exception import StorageAccountCreationException
from pkg.command.azcli_cmd import AzCliCommand
from pkg.constant import Constant
from pkg.creator._creator import Creator
from pkg.entity._az_cli import AzCli
from pkg.executor.azcli._az_cli_executor import AzCliExecutor
from pkg.enums.language._language import Language
from pkg.executor.azcli.command._azcli_cmd_executor import AzCliCommandExecutor
from pkg.utils import _name_creator


class StorageAccountCreator(Creator):
    SKU_NAME = "Standard_LRS"

    def create(self, *args):
        lang: Language = args[0]
        az_cmd: AzCli = AzCli().append("storage ").append("account").append(Constant.CREATE).\
            append("--name").append(_name_creator.create_storage_account(lang)).append(Constant.ARG_LOCATION).\
            append(Constant.REGION).append(Constant.ARG_RG).append(Constant.RESOURCE_GROUP_NAME).\
            append(Constant.ARG_SKU).append(self.SKU_NAME)
        try:
            az_cli_cmd: AzCliCommand = AzCliCommand(az_cmd)
            az_cli_cmd_executor = AzCliCommandExecutor(az_cli_cmd)
            res = az_cli_cmd_executor.execute()
        except Exception as e:
            raise StorageAccountCreationException("Exception occured while creating storage account for lang "+
                                                  lang.name.lower()) from e

        return res