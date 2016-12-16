from enum import Enum

class PebbleEnvelope(object):
    pass 
    
class PebbleEnvelopeType(Enum):
    pebbleList = 0
    status = 1
    message = 2
    deliveryStatus = 3

class pebbleStatusMessage(PebbleEnvelope):
    def __init__(self, sender, status):
        self.type = PebbleEnvelopeType.status.value
        self.status = status
        self.sender = sender
        
    def getAttributes(self):
        return {"EnvelopeType": self.type, "PebbleName": self.sender, "ConnectionStatus": self.status }

class pebblePushMessage(PebbleEnvelope):
    def __init__(self, message, pebbleName):
        self.envelopeType = PebbleEnvelopeType.message.value
        self.uniqueId = None
        self.message = message
        self.pebbleName = pebbleName
        self.readyMessage()

    def getAttributes(self):
        return { "EnvelopeType": self.envelopeType, "TransactionId": self.uniqueId , "ResponseValue": self.message, "PebbleName": self.pebbleName }
        
    def readyMessage(self):
        pressedButton = int.from_bytes(self.message.data.dictionary[0].data, byteorder='little')
        messageType = self.message.data.dictionary[0].key
        self.uniqueId = self.message.data.dictionary[1].data.decode("utf-8")
        if type(pressedButton) is int:
            self.message = pressedButton     
               
class pebbleListEnvelope():
    def __init__(self, pebbleList):
        self.type = PebbleEnvelopeType.pebbleList.value
        self.pebbleList = pebbleList
                
    def getAttributes(self):
        return { "EnvelopeType": self.type, "PebbleList": self.pebbleList }

class deliveryStatusEnvelope(PebbleEnvelope):
    def __init__(self, transactionId, status, pebbleName):
        self.envelopeType = PebbleEnvelopeType.deliveryStatus.value
        self.transactionId = transactionId
        self.status = status
        self.pebbleName = pebbleName

    def getAttributes(self):
        return { "EnvelopeType": self.envelopeType, "TransactionId" : self.transactionId, "DeliveryStatus" : self.status, "PebbleName": self.pebbleName }
