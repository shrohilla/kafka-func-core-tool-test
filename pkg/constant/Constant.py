
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
EVENTHUB_CONNECTION_STRING_TRIGGER = 'Endpoint=sb://shivamehub.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=ymTH6jTEbkxF6YLBKeGf1nEwxl58OlIvv29gWfyEimc=;EntityPath=triggerhub'
EVENTHUB_TRIGGER_NAME = 'triggerhub'
EVENTHUB_BROKER_LIST = 'shivamehub.servicebus.windows.net:9093'
EVENTHUB_CONNECTION_STRING_OUTPUT = 'Endpoint=sb://shivamehub.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=wjQKHHMeE/hyrBOsTPdZVoiuP2JCFhccqoIFRO9v2lE=;EntityPath=outputhub'
EVENTHUB_OUTPUT_NAME = 'outputhub'

HTTPRequest_POST = 'post'
HTTPRequest_GET = 'get'
HTTPRequest_PUT = 'put'

BROKER_LIST = 'BrokerList'
KAFKA_PASSWORD = 'KafkaPassword'
KAFKA_PASSWORD_OUTPUT = 'KafkaPasswordOutput'

FUNCTION_APP = 'functionapp'
KAFKA_TRIGGER = 'KafkaExample'
KAFKA_OUTPUT =  'Kafkaoutput'