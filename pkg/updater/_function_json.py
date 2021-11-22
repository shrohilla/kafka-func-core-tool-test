import json
import logging
import os.path

from pkg.constant import Constant
from pkg.enums.kafka._kafka_platform import KafkaPlatform


class FunctionJsonUpdater():
    _local_setting = "local.settings.json"
    _kafka_trigger = "KafkaExample"
    _kafka_output = "Kafkaoutput"
    _function_setting = "function.json"

    def __init__(self):
        pass

    def update_function_json(self, kafka_platform: KafkaPlatform):
        local_config, trigger_function_config, output_function_config = self._retrieve_config()
        self._build_config(local_config, trigger_function_config, output_function_config, kafka_platform)

    def _retrieve_config(self):
        local_config = self._get_config(self._local_setting)
        trigger_function_config = self._get_config(os.path.join(self._kafka_trigger, self._function_setting))
        output_function_config = self._get_config(os.path.join(self._kafka_output, self._function_setting))
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
            function_config['bindings'][0]['topic'] = Constant.EVENTHUB_NAME
            output_fn_config['bindings'][1]['topic'] = Constant.EVENTHUB_NAME
            output_fn_config['bindings'][0]['authLevel'] = 'anonymous'
            local_config['Values']['BrokerList'] = Constant.EVENTHUB_BROKER_LIST
            local_config['Values']['KafkaPassword'] = Constant.EVENTHUB_CONNECTION_STRING

        self._dump_config(function_config, output_fn_config, local_config)
        pass

    def _dump_config(self, function_config, output_fn_config, local_config):
        logging.info("in _dump_config")
        self._dump_config_file(os.path.join(self._kafka_trigger, self._function_setting), function_config)
        self._dump_config_file(os.path.join(self._kafka_output, self._function_setting), output_fn_config)
        self._dump_config_file(self._local_setting, local_config)
        logging.info("dumping the updated json completed")

    def disable_function_config(self):
        logging.info("in disable function")
        local_config = self._get_config(self._local_setting)
        local_config['Values']['AzureWebJobs.{}.Disabled'.format(self._kafka_trigger)] = 'true'
        local_config['Values']['AzureWebJobs.{}.Disabled'.format(self._kafka_output)] = 'true'
        self._dump_config_file(self._local_setting, local_config)
        logging.info('config dumped in local settings')
