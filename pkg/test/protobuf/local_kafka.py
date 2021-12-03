import json
import os

import certifi
from confluent_kafka import Producer, Consumer, serializing_producer, SerializingProducer, DeserializingConsumer
import time

from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from pkg.test.protobuf.customer_pb2 import Customer

if __name__ == '__main__':

    # Read arguments and configurations and initialize

    topic = "protoCustomer"
    schema_conf = {}
    schema_conf['auto.register.schemas'] = False
    # Create Producer instance
    #producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    producer_conf = {}
    producer_conf['bootstrap.servers'] = 'localhost:9092'
    #producer_conf['security.protocol'] = 'SASL_SSL'
    #producer_conf['value.serializer'] = customer_pb2._sym_db.RegisterMessage
    protobuf_ser: ProtobufSerializer = ProtobufSerializer(Customer, None, schema_conf)
    protobuf_ser._known_subjects.add('protoCustomer-value')
    protobuf_ser._schema_id = 1
    producer_conf['value.serializer'] = protobuf_ser
    #serializing_producer
    producer_conf['security.protocol'] = 'PLAINTEXT'
    producer_conf['sasl.mechanisms'] = 'PLAIN'
    #producer_conf['sasl.username'] = 'USER'
    #producer_conf['sasl.password'] = 'PASSWORD'
    producer_conf.pop('schema.registry.url', None)
    producer_conf.pop('basic.auth.user.info', None)
    producer_conf.pop('basic.auth.credentials.source', None)

    #producer_conf['ssl.ca.location'] = certifi.where()
    #producer = Producer(producer_conf)
    serialize_producer: SerializingProducer = SerializingProducer(producer_conf)
    print("A")

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

    i = 19
    #for n in range(10):
    while i < 20:
        record_key = "alice"
        customer_data: Customer = Customer()
        customer_data.id = 1
        customer_data.name = b'shivam'
        customer_data.username = b'shrohilla'
        customer_data.email_address= b''
        print("Producing record: {}\t{}".format(record_key, i))
        #producer.produce(topic, key=record_key, value=str(i), on_delivery=acked)
        serialize_producer.produce(topic, key=record_key, value=customer_data, on_delivery=acked)
        #producer.poll() #serves delivery reports (on_delivery)
        # from previous produce() calls.
        #producer.poll(0)
        serialize_producer.poll(0)
        i += 1

    #producer.flush()
    serialize_producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))

    time.sleep(1)
    producer_conf['group.id'] = '$Default'
    producer_conf['auto.offset.reset'] = 'latest'
    producer_conf.pop('value.serializer')
    protobuf_de_ser: ProtobufDeserializer = ProtobufDeserializer(Customer)
    #protobuf_deser._known_subjects.add('protoCustomer-value')
    #protobuf_ser._schema_id = 1
    producer_conf['value.deserializer'] = protobuf_de_ser
    consumer = DeserializingConsumer(producer_conf)
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
                record_value: Customer = msg.value()
                #data = json.loads(record_value)
                #print(record_value)
                #count = data['count']
                #total_count += count
                print("Consumed record with key {} and value {}, \
                          and updated total count to {}"
                      .format(record_key, record_value, total_count))
                counter += 1
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()