from enum import Enum


class KafkaPlatform(Enum):
    EVENT_HUB = 0
    CONFLUENT = 1
    # LOCAL