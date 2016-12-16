from data import serverEnvelope, pebbleCommand
import json
from data import serverEnvelope
from Logics import BluetoothManager
import threading


from Logics import WebserviceClient, JSONWrapper
from services import MessageMarshallerService

class serverMessageService():

    _webserviceClient = WebserviceClient.WebserviceClient
    _messageMarshallerService = MessageMarshallerService
    _bluetoothManager = BluetoothManager.BluetoothManager
    _jsonWrapper = JSONWrapper.JSONWrapper
    def __init__(serverMessageService, messageMarshallerService, webserviceClient, bluetoothManager, jsonWrapper):
        _webserviceClient = webserviceClient
        _messageMarshallerService = messageMarshallerService
        _bluetoothManager = bluetoothManager
        _jsonWrapper = jsonWrapper
    
    @staticmethod
    def _encodeMessageForServer(message):
        """Encode outgoing webservice message"""
        print(message.getAttributes())
        return serverMessageService._jsonWrapper.dumps(message.getAttributes())
    
    @staticmethod
    def sendMessageToServer(message):
        """Send message to webservice"""
        if type(message) is not str:
            message = serverMessageService._encodeMessageForServer(message)
        serverMessageService._webserviceClient.send(message)
    
    @staticmethod
    def _readMessageFromServer(message):
        """Read incoming webservice message"""
        messageList = message.split(',')
        messageList = list(filter(None, messageList))
        print(messageList)
        serverMessageService._checkServerMessage(messageList)
        
    @staticmethod
    def _checkServerMessage(message):
        """Check type of incoming webservice message"""
        envelopeType = int(message[0])
        print(envelopeType)
        envelopeTypes = serverEnvelope.serverEnvelopeType 
        if(envelopeType == envelopeTypes.scan.value):
            print("scan")
            scanThread = threading.Thread(target=MessagingService._bluetoothManager.sendAvailablePebblesToServer)
            scanThread.start()
            print("threading")
            return
        if(envelopeType == envelopeTypes.install.value):
            MessagingService._pebbleManager.updatePebbleApp(message[1], message[2])
            return
        elif(envelopeType == envelopeTypes.connect.value) or (envelopeType == serverEnvelope.serverEnvelopeType.disconnect.value):
            targetPebble = message[1]
            envelope = serverEnvelope.serverEnvelope(envelopeType, targetPebble)
            
        elif(envelopeType == envelopeTypes.message.value):
            transactionID = message[1]
            targetPebble = message[2]
            messageType = message[3]
            data = message[4]
            envelope = serverEnvelope.serverEnvelope(envelopeType, transactionID, targetPebble, messageType, data)

        else: MessagingService._webserviceClient.send(MessagingService._errorMessage); return
        
        MessagingService._messageMarshallerService.sendMessageToPebble(envelope)
