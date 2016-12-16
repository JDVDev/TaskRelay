from enum import Enum
class PebbleStatus(Enum):
    unavailable = 0
    available = 1
    connected = 2
    disconnected = 3
    pending =  4
    failed = 5
    