from enum import Enum

class ServerEnvelopeType(Enum):
    scan = 0
    connect = 1
    disconnect = 2
    message = 3
    install = 4
    notification = 5

class ServerEnvelope():
    def __init__(self, envelopeType, target , messageType = None, data = None, note = None, uniqueID = None):
        self.envelopeType = envelopeType
        self.uniqueID = uniqueID        
        self.target = target
        self.messageType = messageType
        self.data = data
        self.note = note