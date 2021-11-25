#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show receiving events from an Event Hub.
"""
import datetime
import os
import threading
import time
from typing import List

from azure.eventhub import EventHubConsumerClient, EventHubProducerClient, EventData

from pkg.constant import Constant

CONNECTION_STR = Constant.EVENTHUB_CONNECTION_STRING_OUTPUT
EVENTHUB_NAME = Constant.EVENTHUB_OUTPUT_NAME


def on_event(partition_context, event):
    # Put your code here.
    # If the operation is i/o intensive, multi-thread will have better performance.
    print("Received event from partition: {}.".format(partition_context.partition_id))


def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))


# def on_partition_close(partition_context, reason):
#     # Put your code here.
#     print("Partition: {} has been closed, reason for closing: {}.".format(
#         partition_context.partition_id,
#         reason
#     ))


def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def closing_consumer_client(consumer_client):
    print("closing client")
    consumer_client.close()
    print("client closed")

def create_producer_send_message():
    producer = EventHubProducerClient.from_connection_string(
            conn_str=CONNECTION_STR,
            eventhub_name=EVENTHUB_NAME
        )
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData('Har Har Mahadev'))
    res = producer.send_batch(event_data_batch)
    producer.close()


if __name__ == '__main__':
    #create_producer_send_message()
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group='$Default',
        eventhub_name=EVENTHUB_NAME,
    )

    # partition_ids: List = consumer_client.get_partition_ids()
    # for partition_id in partition_ids:
    #     partition_details = consumer_client.get_partition_properties(partition_id)
    #     print(partition_details)
    timer = threading.Timer(100, closing_consumer_client, [consumer_client])
    timer.start()
    try:
        with consumer_client:
            consumer_client.receive(
                on_event=on_event,
                on_partition_initialize=on_partition_initialize,
                # on_partition_close=on_partition_close,
                on_error=on_error,
                starting_position=-1,  # "-1" is from the beginning of the partition.
            )
    except KeyboardInterrupt:
        print('Stopped receiving.')
