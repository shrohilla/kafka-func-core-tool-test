from pkg.command.azcli_cmd import AzCliCommand
from pkg.constant import Constant
from pkg.creator._creator import Creator
from pkg.entity._az_cli import AzCli
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.kafka._kafka_platform import KafkaPlatform
from pkg.enums.language._language import Language
from pkg.executor._executor import Executor
from pkg.executor.azcli._az_cli_executor import AzCliExecutor
from pkg.executor.azcli.command._azcli_cmd_executor import AzCliCommandExecutor
from pkg.utils import _name_creator


class FunctionAppConfigCreator(Creator):

    def create(self, *args):
        lang: Language = args[0]
        platform: OSPlatform = args[1]
        kafka_platform: KafkaPlatform = args[2]
        disable_flag = args[3]
        app_name = _name_creator.create_function_app(lang, platform)
        settings = []
        if disable_flag is not None and disable_flag:
            settings.append('AzureWebJobs.{}.Disabled'.format(Constant.KAFKA_TRIGGER)+'=true')
            settings.append('AzureWebJobs.{}.Disabled'.format(Constant.KAFKA_OUTPUT)+'=true')
        if disable_flag is None and KafkaPlatform.EVENT_HUB == kafka_platform:
            settings.append(Constant.BROKER_LIST + '=' + Constant.EVENTHUB_BROKER_LIST)
            settings.append(Constant.KAFKA_PASSWORD + '=' + Constant.EVENTHUB_CONNECTION_STRING_TRIGGER)
            settings.append(Constant.KAFKA_PASSWORD_OUTPUT + '=' + Constant.EVENTHUB_CONNECTION_STRING_OUTPUT)

        return self._execute_publishing_settings(app_name, settings)

    def _execute_publishing_settings(self, app_name, settings):
        az_cli: AzCli = self._create_app_settings(app_name, settings)
        az_cli_cmd: AzCliCommand = AzCliCommand(az_cli)
        az_cli_cmd_executor = AzCliCommandExecutor(az_cli_cmd)
        return az_cli_cmd_executor.execute()

    def _create_app_settings(self, app_name, settings):
        setting_str = ' '.join([str(setting) for setting in settings])
        az_cli: AzCli = AzCli().append(Constant.FUNCTION_APP).append('config').append('appsettings ').\
            append('set').append('--name').append(app_name).append(Constant.ARG_RG).\
            append(Constant.RESOURCE_GROUP_NAME).append('--settings').append(setting_str)
        return  az_cli
