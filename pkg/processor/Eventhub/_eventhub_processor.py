import logging
import threading
import time
from typing import List

from azure.eventhub import EventHubProducerClient, EventData, EventHubConsumerClient

from pkg._exception import ValidationFailedException, EventHubDataNotProcessedException, TestFailedException
from pkg.command._http_cmd import HttpCommand
from pkg.constant import Constant
from pkg.entity._http import HttpRequest
from pkg.executor._executor import Executor
from pkg.executor.http.command._http_cmd_executor import HttpCommandExecutor
from pkg.global_data import _global_data
from pkg.processor._processor import Processor


class EventHubTestProcessor(Processor):

    def validate(self):
        return True

    def post_process(self):
        pass

    def execute_process(self):
        time.sleep(30)
        self._request_on_output_trigger()
        #self._create_producer_send_message()
        time.sleep(5)
        self._check_if_all_message_processed()
        logging.info("EVENT HUB Trigger message processed successfully")

    def _check_if_all_message_processed(self):
        self._consumer_client = EventHubConsumerClient.from_connection_string(
            conn_str=Constant.EVENTHUB_CONNECTION_STRING,
            consumer_group='$Default',
            eventhub_name=Constant.EVENTHUB_NAME,
        )
        timer = threading.Timer(20, self._closing_consumer_client)
        timer.start()
        self._consumer_client.receive(
            on_event=self._on_event,
            #on_partition_initialize=on_partition_initialize,
            # on_partition_close=on_partition_close,
            #on_error=on_error,
            #starting_position="-1",  # "-1" is from the beginning of the partition.
        )

        # partition_ids: List = consumer_client.get_partition_ids()
        # for partition_id in partition_ids:
        #     partition_details = consumer_client.get_partition_properties(partition_id)
        #     if partition_details['beginning_sequence_number'] != partition_details['last_enqueued_sequence_number']:
        #         consumer_client.close()
        #         raise EventHubDataNotProcessedException("test case failed")
        self._consumer_client.close()

    def _create_producer_send_message(self):
        producer = EventHubProducerClient.from_connection_string(
            conn_str=Constant.EVENTHUB_CONNECTION_STRING,
            eventhub_name=Constant.EVENTHUB_NAME
        )
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData('Har Har Mahadev'))
        producer.send_batch(event_data_batch)
        producer.close()

    def cleanup(self):
        pass

    def _request_on_output_trigger(self):
        params = {'message': 'har har mahadev'}
        func_url = _global_data.get('url')+'/api/Kafkaoutput'
        if not func_url.startswith('https://'):
            func_url = 'https://'+func_url
        http_req = HttpRequest(url=func_url, method='get', body={}, params=params)
        http_cmd: HttpCommand = HttpCommand(http_req)
        http_cmd_executor: Executor = HttpCommandExecutor(http_cmd)
        res = http_cmd_executor.execute()
        if res is None or res == '':
            raise TestFailedException('Eventhub output binding test failed')

    def _on_event(self, partition_context, event):
        print("Received event from partition: {}.".format(partition_context.partition_id))
        self._consumer_client.close()
        raise EventHubDataNotProcessedException("test case failed")

    def _closing_consumer_client(self):
        print("closing client")
        self._consumer_client.close()
        print("client closed")
