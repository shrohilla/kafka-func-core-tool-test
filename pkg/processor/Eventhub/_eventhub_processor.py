import logging
import threading
import time

from azure.eventhub import EventHubProducerClient, EventData, EventHubConsumerClient
from requests import Response

from pkg._exception import ValidationFailedException, EventHubDataNotProcessedException, TestFailedException
from pkg.command._http_cmd import HttpCommand
from pkg.constant import Constant
from pkg.entity._http import HttpRequest
from pkg.executor._executor import Executor
from pkg.executor.http.command._http_cmd_executor import HttpCommandExecutor
from pkg.global_data import _global_data
from pkg.processor._processor import Processor


class EventHubTestProcessor(Processor):
    _output_msg = 'har har mahadev'

    def validate(self):
        return True

    def post_process(self):
        pass

    def execute_process(self):
        time.sleep(30)
        self._validate_output_trigger()
        time.sleep(5)
        self._validate_trigger()
        logging.info("EVENT HUB Trigger message processed successfully")

    def _create_event_hub_consumer(self, conn_str, eventhub_name):
        consumer_client = EventHubConsumerClient.from_connection_string(
            conn_str=conn_str, consumer_group='$Default', eventhub_name=eventhub_name,
        )
        return consumer_client


    def _create_producer_send_message(self):
        producer = EventHubProducerClient.from_connection_string(
            conn_str=Constant.EVENTHUB_CONNECTION_STRING_TRIGGER,
            eventhub_name=Constant.EVENTHUB_TRIGGER_NAME
        )
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData('Har Har Mahadev'))
        producer.send_batch(event_data_batch)
        producer.close()

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

    def _on_event_output(self, partition_context, event):
        print("Received event from partition: {}.".format(partition_context.partition_id))
        self._event_hub_output_consumer.close()

    def _closing_consumer_client(self, event_consumer):
        print("closing client")
        event_consumer.close()
        print("client closed")

    def _validate_output_trigger(self):
        self._request_on_output_trigger()
        if not self._validate_msg_output_trigger():
            raise ValidationFailedException('Eventhub trigger failed')
        pass

    def _validate_msg_output_trigger(self):
        event_hub_consumer = self._create_event_hub_consumer(Constant.EVENTHUB_CONNECTION_STRING_OUTPUT,
                                        Constant.EVENTHUB_OUTPUT_NAME)
        event_hub_consumer.receive(
            on_event=self._on_event_output,
            # on_partition_initialize=on_partition_initialize,
            # on_partition_close=on_partition_close,
            # on_error=on_error,
            # starting_position="-1",  # "-1" is from the beginning of the partition.
        )
        self._event_hub_output_consumer = event_hub_consumer
        timer = threading.Timer(10, self._closing_consumer_client, [event_hub_consumer])
        timer.start()

        return True

    def _validate_trigger(self):
        self._create_producer_send_message()
        event_hub_consumer = self._create_event_hub_consumer(Constant.EVENTHUB_CONNECTION_STRING_TRIGGER,
                                        Constant.EVENTHUB_TRIGGER_NAME)
        event_hub_consumer.receive(
            on_event=self._on_event,
            # on_partition_initialize=on_partition_initialize,
            # on_partition_close=on_partition_close,
            # on_error=on_error,
            # starting_position="-1",  # "-1" is from the beginning of the partition.
        )
        self._event_hub_output_consumer = event_hub_consumer
        timer = threading.Timer(10, self._closing_consumer_client, [event_hub_consumer])
        timer.start()
        return True

    def _on_event(self, partition_context, event):
        print("Received event from partition: {}.".format(partition_context.partition_id))
        self._event_hub_output_consumer.close()
        raise EventHubDataNotProcessedException("test case failed")
