from libpebble2.protocol import AppMessageACK, AppMessageNACK
from libpebble2.services.appmessage import AppMessage

#type
from uuid import UUID
import threading

import time
from libpebble2.protocol.appmessage import AppMessagePush
from data.DeliveryStatus import DeliveryStatus
import libpebble2
from data.PebbleStatus import PebbleStatus

class Pebble():
    def __init__(self, name, connectionFactory, messageServiceFactory, appStartService, outgoingPebbleMessageService):
        self.name = name
        self.deliverStatus = None
        self.uuid = UUID("2A8A4EF9-99C4-47FD-8DBF-428C89DE6F6E")
        self.connectionFactory = connectionFactory
        self.messageServiceFactory = messageServiceFactory
        self.appStartService = appStartService
        self._outgoingPebbleMessageService = outgoingPebbleMessageService
        self.resending = False
        self.pebbleThread = None
        self.mostRecentMessage = None
        self.transactionId = None
        self.AppMessageService = None
        self.pebbleConnection = None
    
    def startAppMessageService(self):
        """Start appmessage service (protocol used to communicate with pebble applications)"""
        self.AppMessageService = self.messageServiceFactory.produceAppMessageService(self.pebbleConnection)
        self.pebbleConnection.register_endpoint(AppMessage , lambda message : self.appMessageHandler(message, self.pebbleConnection))
    
    def sendAppMessage(self, messageType, messageString, messageID, messageList = None):
        """Send appmessage to Pebble, notify the webservice if message attempt results in a NACK"""
        if(type(messageString) is str):
            self.transactionId = messageID
            self.mostRecentMessage = self.messageServiceFactory.produceAppMessage(messageType, messageString, messageID, messageList)
        else: self.mostRecentMessage = messageString
        try:
            self.AppMessageService.send_message(self.uuid, self.mostRecentMessage)
        except:
            self._outgoingPebbleMessageService.sendDeliveryStatusToMarshaller(self.transactionId, DeliveryStatus.NACK.value, self.name)
            self.disconnect()

    def connect(self):
        self.pebbleConnection = self.connectionFactory.produceSerial(self.name)
        self.pebbleConnection.connect()
        if self.pebbleConnection.connected:
            try:
                self.pebbleConnection.run_async()
                runningThreads = threading.active_count()
                self.pebbleThread = threading.enumerate()[runningThreads - 1]
                self.startAppMessageService()
                return self.pebbleConnection.connected
            except libpebble2.exceptions.TimeoutError:
                return False

    def disconnect(self):
        """Disconnect pebble (No official way to disconnect from pebble in libpebble2 documentation)"""
        self.pebbleConnection.transport.connection.close() 
            
    def appMessageHandler(self, message, pebble): 
        """Handle incoming pebble messages"""
        messageType = type(message.data)
        if messageType is AppMessageACK:
            print("ACK")
            self.deliverStatus = True
            self.resending = False
            self._outgoingPebbleMessageService.sendDeliveryStatusToMarshaller(self.transactionId, DeliveryStatus.ACK.value, self.name)
        elif messageType is AppMessageNACK:
            print("NACK")
            self.retrySendingMessage()
        elif messageType is AppMessagePush:
            print("PUSH")
            self._outgoingPebbleMessageService.sendPushMessageToMarshaller(message, self.name)
        return self.deliverStatus    
    
    def retrySendingMessage(self):
        if self.resending == False:
            self.resending = True
            self.appStartService.openApp(self.pebbleConnection, self.uuid)
            time.sleep(5)
            self.AppMessageService.send_message(self.uuid, self.mostRecentMessage)
        else:
            self._outgoingPebbleMessageService.sendDeliveryStatusToMarshaller(self.transactionId, DeliveryStatus.NACK.value, self.name)
            self.resending = False
