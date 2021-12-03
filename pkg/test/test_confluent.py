import json
import os
import time

import certifi
from confluent_kafka import Producer, Consumer

if __name__ == '__main__':

    # Read arguments and configurations and initialize

    topic = "v4_test"
    # Create Producer instance
    #producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    producer_conf = {}
    producer_conf['bootstrap.servers'] = 'pkc-epwny.eastus.azure.confluent.cloud:9092'
    producer_conf['security.protocol'] = 'SASL_SSL'
    producer_conf['sasl.mechanisms'] = 'PLAIN'
    producer_conf['sasl.username'] = os.environ['confluent_user_name']
    producer_conf['sasl.password'] = os.environ['confluent_secret']
    producer_conf.pop('schema.registry.url', None)
    producer_conf.pop('basic.auth.user.info', None)
    producer_conf.pop('basic.auth.credentials.source', None)

    producer_conf['ssl.ca.location'] = certifi.where()
    producer = Producer(producer_conf)

    # Create topic if needed
    #ccloud_lib.create_topic(conf, topic)

    delivered_records = 0

    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    def acked(err, msg):
        global delivered_records
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    i = 11
    #for n in range(10):
    while i < 20:
        record_key = "alice"
        #record_value = json.dumps({'count': n})
        record_value = json.dumps({'count': i})
        print("Producing record: {}\t{}".format(record_key, record_value))
        producer.produce(topic, key=record_key, value=record_value, on_delivery=acked)
        #producer.poll() #serves delivery reports (on_delivery)
        # from previous produce() calls.
        producer.poll(0)
        i += 1

    producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))

    time.sleep(1)
    producer_conf['group.id'] = '$Default'
    producer_conf['auto.offset.reset'] = 'latest'
    consumer = Consumer(producer_conf)
    consumer.subscribe([topic])
    total_count = 0
    counter = 0
    try:
        while True:
            msg = consumer.poll(1)
            if counter >= 9:
                consumer.close()
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = msg.key()
                record_value = msg.value()
                data = json.loads(record_value)
                count = data['count']
                total_count += count
                print("Consumed record with key {} and value {}, \
                          and updated total count to {}"
                      .format(record_key, record_value, total_count))
                counter += 1
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
