import json
import logging
import os.path

from pkg.constant import Constant
from pkg.enums.kafka._kafka_platform import KafkaPlatform


class FunctionJsonUpdater:
    _local_setting = "local.settings.json"
    _function_setting = "function.json"

    def update_function_json(self, kafka_platform: KafkaPlatform):
        local_config, trigger_function_config, output_function_config = self._retrieve_config()
        self._build_config(local_config, trigger_function_config, output_function_config, kafka_platform)

    def _retrieve_config(self):
        local_config = self._get_config(self._local_setting)
        trigger_function_config = self._get_config(os.path.join(Constant.KAFKA_TRIGGER, self._function_setting))
        output_function_config = self._get_config(os.path.join(Constant.KAFKA_OUTPUT, self._function_setting))
        return local_config, trigger_function_config, output_function_config

    def _get_config(self, config_file):
        with open(config_file, 'r') as f:
            data = f.read()
            config = json.loads(data)
            return config

    def _dump_config_file(self, config_file, data):
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=4)

    def _build_config(self, local_config, function_config, output_fn_config, kafka_platform):
        if KafkaPlatform.EVENT_HUB == kafka_platform:
            self._build_event_hub_kafka_config(function_config, local_config, output_fn_config)
        elif KafkaPlatform.CONFLUENT == kafka_platform:
            self._build_confluent_kafka_config(function_config, local_config, output_fn_config)

        self._dump_config(function_config, output_fn_config, local_config)

    def _build_confluent_kafka_config(self, function_config, local_config, output_fn_config):
        function_config['bindings'][0]['topic'] = Constant.CONFLUENT_TRIGGER_NAME
        function_config['bindings'][0]['username'] = Constant.CONFLUENT_USER_NAME
        output_fn_config['bindings'][1]['topic'] = Constant.CONFLUENT_OUTPUT_NAME
        output_fn_config['bindings'][1]['username'] = Constant.CONFLUENT_USER_NAME
        output_fn_config['bindings'][1]['password'] = Constant.KAFKA_PASSWORD
        output_fn_config['bindings'][0]['authLevel'] = 'anonymous'
        local_config['Values'][Constant.BROKER_LIST] = Constant.CONFLUENT_BROKER_LIST
        local_config['Values'][Constant.KAFKA_PASSWORD] = Constant.CONFLUENT_CONNECTION_STRING
        local_config['Values'][Constant.KAFKA_PASSWORD_OUTPUT] = Constant.CONFLUENT_CONNECTION_STRING

    def _build_event_hub_kafka_config(self, function_config, local_config, output_fn_config):
        function_config['bindings'][0]['topic'] = Constant.EVENTHUB_TRIGGER_NAME
        output_fn_config['bindings'][1]['topic'] = Constant.EVENTHUB_OUTPUT_NAME
        output_fn_config['bindings'][1]['password'] = Constant.KAFKA_PASSWORD_OUTPUT
        output_fn_config['bindings'][0]['authLevel'] = 'anonymous'
        local_config['Values'][Constant.BROKER_LIST] = Constant.EVENTHUB_BROKER_LIST
        local_config['Values'][Constant.KAFKA_PASSWORD] = Constant.EVENTHUB_CONNECTION_STRING_TRIGGER
        local_config['Values'][Constant.KAFKA_PASSWORD_OUTPUT] = Constant.EVENTHUB_CONNECTION_STRING_OUTPUT

    def _dump_config(self, function_config, output_fn_config, local_config):
        logging.info("in _dump_config")
        self._dump_config_file(os.path.join(Constant.KAFKA_TRIGGER, self._function_setting), function_config)
        self._dump_config_file(os.path.join(Constant.KAFKA_OUTPUT, self._function_setting), output_fn_config)
        self._dump_config_file(self._local_setting, local_config)
        logging.info("dumping the updated json completed")

    def disable_function_config(self):
        logging.info("in disable function")
        local_config = self._get_config(self._local_setting)
        local_config['Values']['AzureWebJobs.{}.Disabled'.format(Constant.KAFKA_TRIGGER)] = 'true'
        local_config['Values']['AzureWebJobs.{}.Disabled'.format(Constant.KAFKA_OUTPUT)] = 'true'
        self._dump_config_file(self._local_setting, local_config)
        logging.info('config dumped in local settings')
