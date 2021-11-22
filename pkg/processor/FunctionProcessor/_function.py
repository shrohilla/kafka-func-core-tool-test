import logging

from pkg._exception import ValidationFailedException
from pkg.creator._creator import Creator
from pkg.enums.kafka._kafka_platform import KafkaPlatform
from pkg.factory.creator import _creator
from pkg.creator.type._creator_type import CreatorType
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.language._language import Language
from pkg.factory.creator._creator import CreatorFactory
from pkg.processor.Eventhub._eventhub_processor import EventHubTestProcessor
from pkg.processor._processor import Processor
import os

from pkg.publisher._publisher import FunctionPublisher
from pkg.updater._function_json import FunctionJsonUpdater


class FunctionProcessor(Processor):
    _app_name = "kafkaexttest-"

    def __init__(self, path, os_platform: OSPlatform):
        self._path = path
        self._os_platform = os_platform
        self._factory: CreatorFactory = _creator.get_instance()
        self._config_updater: FunctionJsonUpdater = FunctionJsonUpdater()
        self._function_app_publisher: FunctionPublisher = FunctionPublisher()
        self._event_hub_test_processor: Processor = EventHubTestProcessor()

    def validate(self):
        return True

    def pre_process(self):
        if not self.validate():
            raise ValidationFailedException("validation failed")
        pass

    def execute_process(self):
        for lang in Language:
            if Language.PYTHON == lang and OSPlatform.WINDOW == self._os_platform:
                continue
            if OSPlatform.LINUX == self._os_platform and Language.POWERSHELL == lang:
                continue
            self._create_azure_resources(self._os_platform, lang)
            for kafka_platform in KafkaPlatform:
                folder_path = self._build_function_folder(lang)
                os.chdir(folder_path)
                self._create_local_function(folder_path, self._os_platform, lang)
                self._update_json_function(kafka_platform)
                #os.chdir(func_folder_path)
                self._function_app_publisher.publish(lang, self._os_platform)
                self._process_test(kafka_platform, self._os_platform, lang)
                self._function_disable(self._os_platform, lang)

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

    def _process_test(self, kafka_platform, os_platform, lang):
        if KafkaPlatform.EVENT_HUB == kafka_platform:
            self._event_hub_test_processor.execute_process()
            logging.info("event hub test processed successfully for {} on {}".format(lang, os_platform))

    def _function_disable(self, _os_platform, lang):
        self._config_updater.disable_function_config()
        logging.info("re-publishing app after adding disable")
        self._function_app_publisher.publish(lang, self._os_platform)
        logging.info("re-published app after disabling")
        pass