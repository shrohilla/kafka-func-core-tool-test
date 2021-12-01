import logging

from pkg._exception import ValidationFailedException
from pkg.command.azcli_cmd import AzCliCommand
from pkg.constant import Constant
from pkg.creator._config._azure_fn_config_creator import FunctionAppConfigCreator
from pkg.creator._creator import Creator
from pkg.creator.type._creator_type import CreatorType
from pkg.entity._az_cli import AzCli
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.kafka._kafka_platform import KafkaPlatform
from pkg.enums.language._language import Language
from pkg.executor.azcli.command._azcli_cmd_executor import AzCliCommandExecutor
from pkg.factory.creator import _creator
from pkg.factory.creator._creator import CreatorFactory
from pkg.processor._processor import Processor
from pkg.processor.kafka._kafka_processor import KafkaTestProcessor
from pkg.publisher._publisher import Publisher
from pkg.publisher.function._az_function_app_publisher import FunctionAppPublisher
from pkg.updater._function_json import FunctionJsonUpdater

import os

from pkg.utils import _name_creator


class LanguageProcessor(Processor):
    _app_name = "kafkaexttest-"

    def __init__(self, path, os_platform: OSPlatform, lang: Language):
        self._path = path
        self._os_platform = os_platform
        self._factory: CreatorFactory = _creator.get_instance()
        self._config_updater: FunctionJsonUpdater = FunctionJsonUpdater()
        self._function_app_publisher: Publisher = FunctionAppPublisher()
        self._function_app_setting_creator: Creator = FunctionAppConfigCreator()
        self._lang = lang

    def validate(self):
        return True

    def pre_process(self):
        if not self.validate():
            raise ValidationFailedException("validation failed")
        self._create_azure_resources(self._os_platform, self._lang)

    def execute_process(self):
        for kafka_platform in KafkaPlatform:
            folder_path = self._pre_process_folder_function_app()
            self._create_local_function(folder_path, self._os_platform, self._lang)
            self._update_json_function(kafka_platform)
            self._create_setting_functions_app(self._lang, self._os_platform, kafka_platform)
            self._function_app_publisher.publish(self._lang, self._os_platform)
            self._process_test(kafka_platform, self._os_platform, self._lang)

    def _pre_process_folder_function_app(self):
        folder_path = self._build_function_folder(self._lang)
        os.chdir(folder_path)
        return folder_path

    def _build_function_folder(self, lang):
        logging.info("path :: " + self._path)
        app_name = self._app_name + lang.name.lower()
        folder_path = os.path.join(self._path, app_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def _create_azure_resources(self, platform, lang):
        az_res_creator: Creator = self._factory.retrieve_instance(CreatorType.AZURE_RESOURCE)
        az_res_creator.create(lang, platform, self._factory)

    def _create_local_function(self, path, os_platform, lang):
        local_fn_creator: Creator = self._factory.retrieve_instance(CreatorType.LOCAL_FUNCTION)
        local_fn_creator.create(path, lang, os_platform)
        logging.info("local function created successfully")

    def _update_json_function(self, kafka_platform):
        self._config_updater.update_function_json(kafka_platform)

    def _process_test(self, kafka_platform: KafkaPlatform, os_platform, lang):
        kafka_test_processor: Processor = KafkaTestProcessor(os_platform, kafka_platform)
        if kafka_test_processor.execute_process():
            logging.info('{} test processed successfully for {} on {}'.format(kafka_platform.name.lower(),
                                                                              lang, os_platform))

    def _function_disable(self, _os_platform, lang):
        logging.info('updating the disable variable')
        self._function_app_setting_creator.create(lang, _os_platform, None, True)
        logging.info('disable variable updated in function app in azure')
        self._function_app_restart(lang, _os_platform)
        logging.info('restarted app successfully')

    def _create_setting_functions_app(self, lang, platform, kafka_platform):
        logging.info('creating app setting in azure')
        self._function_app_setting_creator.create(lang, platform, kafka_platform, None)
        logging.info('app setting created successfully in azure')

    def _function_app_restart(self, lang: Language, os_platform: OSPlatform):
        az_cli: AzCli = AzCli().append(Constant.FUNCTION_APP).append('restart').append('--name'). \
            append(_name_creator.create_function_app(lang, os_platform)).append(Constant.ARG_RG). \
            append(Constant.RESOURCE_GROUP_NAME)
        az_cli_cmd: AzCliCommand = AzCliCommand(az_cli)
        az_cli_executor: AzCliCommandExecutor = AzCliCommandExecutor(az_cli_cmd)
        az_cli_executor.execute()
        pass

    def post_process(self):
        self._function_disable(self._os_platform, self._lang)
