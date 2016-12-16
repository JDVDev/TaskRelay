from services.OutgoingMessageService import OutgoingMessageService
from data import PebbleEnvelope
from injector import inject, singleton

class OutgoingPebbleMessageService(object):
    @singleton
    @inject(outgoingMessageService = OutgoingMessageService)
    def __init__(self, outgoingMessageService):
        self._outGoingMessageService = outgoingMessageService

    def sendMessageToMarshaller(self, message):
        self._outGoingMessageService.sendMessageToServer(message)

    def sendStatusToMarshaller(self, sender, type):
        statusMessage = PebbleEnvelope.pebbleStatusMessage(sender, type)
        self.sendMessageToMarshaller(statusMessage)
    
    def sendDeliveryStatusToMarshaller(self, transactionId, deliveryStatus, pebbleName):
        deliveryStatusEnvelope = PebbleEnvelope.deliveryStatusEnvelope(transactionId, deliveryStatus, pebbleName)
        self.sendMessageToMarshaller(deliveryStatusEnvelope)
    
    def sendPushMessageToMarshaller(self, message, pebbleName):
        pushMessage = PebbleEnvelope.pebblePushMessage(message, pebbleName)
        print(pushMessage)
        self.sendMessageToMarshaller(pushMessage)
        
    def sendPebbleListToMarshaller(self, pebbleDict):
        pebbleList = PebbleEnvelope.pebbleListEnvelope(pebbleDict)
        self.sendMessageToMarshaller(pebbleList)

