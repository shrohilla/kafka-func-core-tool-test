import json
import logging
import threading
import time
from builtins import Exception

import certifi
from confluent_kafka import Consumer, Producer, Message
from requests import Response

from pkg._exception import ValidationFailedException, EventHubDataNotProcessedException, TestFailedException, \
    NoMessageFoundException
from pkg.command._http_cmd import HttpCommand
from pkg.constant import Constant
from pkg.entity._http import HttpRequest
from pkg.enums.Platform._platform import OSPlatform
from pkg.enums.kafka._kafka_platform import KafkaPlatform
from pkg.executor._executor import Executor
from pkg.executor.http.command._http_cmd_executor import HttpCommandExecutor
from pkg.global_data import _global_data
from pkg.processor._processor import Processor


class KafkaTestProcessor(Processor):
    _output_msg = 'har har mahadev'

    def __init__(self, os_platform: OSPlatform, kafka_platform: KafkaPlatform):
        self._kafka_platform = kafka_platform

    def validate(self):
        return True

    def post_process(self):
        pass

    def execute_process(self):
        time.sleep(30)
        kafka_config = self._create_config()
        self._validate_output_trigger(kafka_config)
        time.sleep(5)
        self._validate_trigger()
        logging.info("EVENT HUB Trigger message processed successfully")
        return True

    def cleanup(self):
        pass

    def _request_on_output_trigger(self):
        params = {'message': self._output_msg}
        func_url = _global_data.get('url')+'/api/Kafkaoutput'
        if not func_url.startswith('https://'):
            func_url = 'https://'+func_url
        http_req = HttpRequest(url=func_url, method='get', body={}, params=params)
        http_cmd: HttpCommand = HttpCommand(http_req)
        http_cmd_executor: Executor = HttpCommandExecutor(http_cmd)
        res: Response = http_cmd_executor.execute()
        if res is None or res.status_code != 200:
            raise TestFailedException('Eventhub output binding test failed, status_code :: {} and reason :: {}'
                                      .format(str(res.status_code), res.reason))
        logging.info('request sent to http endpoint')

    def _on_event_output(self, partition_context, event):
        print("Received event from partition: {}.".format(partition_context.partition_id))
        self._event_hub_output_consumer.close()

    def _validate_output_trigger(self, kafka_config):
        timer = threading.Timer(30, self._request_on_output_trigger)
        timer.start()
        #self._request_on_output_trigger()
        topic = Constant.EVENTHUB_OUTPUT_NAME
        passwd = Constant.EVENTHUB_CONNECTION_STRING_OUTPUT
        conn_str = Constant.EVENTHUB_CONNECTION_STRING_OUTPUT
        if KafkaPlatform.CONFLUENT == self._kafka_platform:
            passwd = Constant.EVENTHUB_CONNECTION_STRING_OUTPUT
            topic = Constant.CONFLUENT_OUTPUT_NAME
            conn_str = Constant.CONFLUENT_CONNECTION_STRING
        if not self._validate_msg_output_trigger(kafka_config, topic, conn_str):
            raise ValidationFailedException('{} trigger failed'.format(self._kafka_platform.name.lower()))


    def _validate_msg_output_trigger(self, kafka_config, topic, passwd):
        kafka_config['group.id'] = "azfunc"
        kafka_config['auto.offset.reset'] = 'latest'
        kafka_config['sasl.password'] = passwd
        consumer = Consumer(kafka_config)
        consumer.subscribe([topic])
        return self._validate_msg_consumed(consumer)

    def _producer_ack(self, err, msg):
        if err:
            raise Exception('Message Delivery Failed for {} for testing TRIGGER \n ERR :: [{}]'.format(
                self._kafka_platform.name.lower(), err))
        logging.info("Produced record to topic {} partition [{}] @ offset {}"
              .format(msg.topic(), msg.partition(), msg.offset()))

    def _validate_trigger(self):
        self._write_on_trigger()
        time.sleep(5)
        kafka_config = self._create_config()
        topic = Constant.EVENTHUB_TRIGGER_NAME
        passwd = Constant.EVENTHUB_CONNECTION_STRING_TRIGGER
        if KafkaPlatform.CONFLUENT == self._kafka_platform:
            topic = Constant.CONFLUENT_TRIGGER_NAME
            passwd = Constant.CONFLUENT_CONNECTION_STRING
        try:
            self._validate_msg_output_trigger(kafka_config, topic, passwd)
        except Exception as e:
            return True


    def _write_on_trigger(self):
        kafka_config = self._create_config()
        topic = Constant.EVENTHUB_TRIGGER_NAME
        kafka_config['sasl.password'] = Constant.EVENTHUB_CONNECTION_STRING_TRIGGER
        if KafkaPlatform.CONFLUENT == self._kafka_platform:
            kafka_config['sasl.password'] = Constant.CONFLUENT_CONNECTION_STRING
            topic = Constant.CONFLUENT_TRIGGER_NAME
        producer = Producer(kafka_config)
        producer.produce(topic, self._output_msg, callback=self._producer_ack)
        producer.poll(10)
        producer.flush()

    def _create_config(self):
        kafka_conf = {}
        kafka_conf['bootstrap.servers'] = Constant.EVENTHUB_BROKER_LIST
        if KafkaPlatform.CONFLUENT == self._kafka_platform:
            kafka_conf['bootstrap.servers'] = Constant.CONFLUENT_BROKER_LIST
        kafka_conf['security.protocol'] = 'SASL_SSL'
        kafka_conf['sasl.mechanisms'] = 'PLAIN'
        if KafkaPlatform.EVENT_HUB == self._kafka_platform:
            kafka_conf['sasl.username'] = '$ConnectionString'
        elif KafkaPlatform.CONFLUENT == self._kafka_platform:
            kafka_conf['sasl.username'] = Constant.CONFLUENT_USER_NAME
        kafka_conf.pop('schema.registry.url', None)
        kafka_conf.pop('basic.auth.user.info', None)
        kafka_conf.pop('basic.auth.credentials.source', None)
        kafka_conf['ssl.ca.location'] = certifi.where()
        return kafka_conf

    def _validate_msg_consumed(self, consumer):
        timeout = time.time() + 180
        try:
            while True:
                if time.time() > timeout:
                    raise NoMessageFoundException('No Message found in consumer for {}'.format(self._kafka_platform.name.lower()))
                msg: Message = consumer.poll(0)
                if msg is None:
                    #logging.info('no message')
                    continue
                elif msg.error():
                    logging.error('error: {}'.format(msg.error()))
                else:
                    # Check for Kafka message
                    logging.info('message found')
                    record_key = msg.key()
                    record_value = msg.value()
                    if self._output_msg in str(record_value):
                        return True
                    else:
                        return False
        finally:
            consumer.close()
