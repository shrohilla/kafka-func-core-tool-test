import os

ARG_LOCATION = "--location"
REGION = "EASTUS"
ARG_RG = "--resource-group"
ARG_SKU = "--sku"
RESOURCE_GROUP_NAME = "kafka-funcapps-new"
CREATE = "create"
UPDATE = "update"
STORAGE_ACCOUNT_NAME = "storekafkaext"
APP_PLAN_NAME = "kafkaextpremiumplan"
FUNCTION_VERSION = "4"

HTTPRequest_POST = 'post'
HTTPRequest_GET = 'get'
HTTPRequest_PUT = 'put'

BROKER_LIST = 'BrokerList'
KAFKA_PASSWORD = 'KafkaPassword'
KAFKA_PASSWORD_OUTPUT = 'KafkaPasswordOutput'

FUNCTION_APP = 'functionapp'
KAFKA_TRIGGER = 'KafkaExample'
KAFKA_OUTPUT = 'Kafkaoutput'

EVENTHUB_CONNECTION_STRING_TRIGGER = os.environ['eventhub_trigger_secret']
EVENTHUB_TRIGGER_NAME = 'triggerhub'
EVENTHUB_BROKER_LIST = os.environ['eventhub_broker_list']
EVENTHUB_CONNECTION_STRING_OUTPUT = os.environ['eventhub_output_secret']
EVENTHUB_OUTPUT_NAME = 'outputhub'

CONFLUENT_BROKER_LIST = os.environ['confluent_broker_list']
CONFLUENT_CONNECTION_STRING = os.environ['confluent_secret']
CONFLUENT_TRIGGER_NAME = 'v4_test'
CONFLUENT_OUTPUT_NAME = 'v4_test_out'
CONFLUENT_USER_NAME = os.environ['confluent_user_name']