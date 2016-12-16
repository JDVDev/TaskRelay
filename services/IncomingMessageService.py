from Logics.BluetoothManager import BluetoothManager
from data import ServerEnvelope, PebbleCommand
from services.IncomingPebbleMessageService import IncomingPebbleMessageService
from injector import inject, singleton
import threading

class IncomingMessageService(object):
    @singleton
    @inject(bluetoothManager = BluetoothManager, incomingPebbleMessageService = IncomingPebbleMessageService)
    def __init__(self, bluetoothManager, incomingPebbleMessageService):
        self._bluetoothManager = bluetoothManager
        self._incomingPebbleMessageService = incomingPebbleMessageService

    def HandleIncomingMessage(self, message):
        if self._readMessageFromServer(message) == False: return False
    
    def _readMessageFromServer(self, message):
        try:
            messageList = message.split(',')
            messageList = list(filter(None, messageList))
        except:
            return False

        if(self._checkServerMessage(messageList) == False):
            return False

    def _checkServerMessage(self, message):
        """Check type of received webservice message and handle accordingly"""
        envelopeType = int(message[0])
        envelopeTypes = ServerEnvelope.ServerEnvelopeType 
        if(envelopeType == envelopeTypes.scan.value):
            """Scan for Pebbles""""
            self._HandleScanCommand()
            return
        if(envelopeType == envelopeTypes.install.value):
            """Install Pebble application"""
            targetPebble = message[1]
            url = message[2]
            envelope = self._HandleInstallCommand(targetPebble, url)

        elif(envelopeType == envelopeTypes.connect.value) or (envelopeType == ServerEnvelope.ServerEnvelopeType.disconnect.value):
            """Connect/Disconnect Pebble"""
            targetPebble = message[1]
            envelope = self._HandleConnectionCommand(envelopeType, targetPebble)
            
        elif(envelopeType == envelopeTypes.message.value):
            """Send message to specific Pebble applicaiton"""
            envelope = self._HandleMessagingCommand(message)

        elif(envelopeType == envelopeTypes.notification.value):
            """Send notification to Pebble. This message will pop-up regardless of opened application"""
            targetPebble = message[1]
            notification = message[2]

            envelope = self._HandleNotificationCommand(targetPebble, notification)

        else: return False

        self._incomingPebbleMessageService.sendMessageToPebble(envelope)

    def _HandleScanCommand(self):
        """Scan for available pebbles"""
        scanThread = threading.Thread(target=self._bluetoothManager.sendAvailablePebblesToServer)
        scanThread.start()

    def _HandleInstallCommand(self, targetPebble, url):
        """Download pebble app from given url and install it on given Pebble"""
        return ServerEnvelope.ServerEnvelope(ServerEnvelope.ServerEnvelopeType.install.value, target = targetPebble, data = url)

    def _HandleConnectionCommand(self, envelopeType, targetPebble):
        """Notify webservice of pebble connection/disconnect"""
        return ServerEnvelope.ServerEnvelope(envelopeType, targetPebble)

    def _HandleMessagingCommand(self, message):
        """Check type of message to be delivered to Pebble"""
        targetPebble = message[1]
        messageType = int(message[2])
        messageString = message[3]
        if(messageType == 1): 
            listItems = message[4]
            transactionId = message[5]
            return ServerEnvelope.ServerEnvelope( ServerEnvelope.ServerEnvelopeType.message.value, targetPebble, messageType, data = messageString, note = listItems, uniqueID = transactionId)
        else:
            transactionID = message[4]
            return ServerEnvelope.ServerEnvelope(envelopeType =  ServerEnvelope.ServerEnvelopeType.message.value, target = targetPebble, messageType = messageType, data = messageString, uniqueID = transactionID)

    def _HandleNotificationCommand(self, targetPebble, notification):
        """Send notifcation to given Pebble"""
        return ServerEnvelope.ServerEnvelope(ServerEnvelope.ServerEnvelopeType.notification.value, targetPebble, data = notification)