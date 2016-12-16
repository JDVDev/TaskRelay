from Logics.PebbleManager import PebbleManager
from data import ServerEnvelope, PebbleCommand
import threading
from injector import inject, singleton
import time

class IncomingPebbleMessageService(object):
    @singleton
    @inject(pebbleManager = PebbleManager)
    def __init__(self, pebbleManager):
        self._pebbleManager = pebbleManager

    def sendMessageToPebble(self, message):  
        """Handle different types of outgoing pebble messages"""
        if message.envelopeType == ServerEnvelope.ServerEnvelopeType.message.value: self._sendAppMessageToPebble(message)
        elif message.envelopeType == ServerEnvelope.ServerEnvelopeType.disconnect.value: self._sendDisconnectCommand(message)
        elif message.envelopeType == ServerEnvelope.ServerEnvelopeType.install.value: self._sendInstallCommand(message)
        elif message.envelopeType == ServerEnvelope.ServerEnvelopeType.connect.value: 
            connectThread = threading.Thread(target=self._sendConnectCommand,args=(message,))
            connectThread.start()
        elif message.envelopeType == ServerEnvelope.ServerEnvelopeType.notification.value: self._sendNotification(message, message.data)

    def _checkAvailabilityOfPebble(self, pebbleAddress):
        """Check if given pebble is currently available"""
        if not self._pebbleManager._getPebble(pebbleAddress): return False

    def _sendAppMessageToPebble(self, message):
        """Send message to pebble application, disconnect Pebble and notify webservice if not succesful"""
        targetPebble = self._pebbleManager._getPebble(message.target)
        try:
            if(message.note): 
                targetPebble.sendAppMessage(message.messageType, message.data, message.uniqueID, message.note); return
            targetPebble.sendAppMessage(message.messageType, message.data, message.uniqueID)
        except:
            self._pebbleManager.disconnectFromPebble(message.target)

    def _sendDisconnectCommand(self, message):
        """disconnect pebble"""
        self._pebbleManager.disconnectFromPebble(message.target)     

    def _sendConnectCommand(self, message):
        """connect to pebble"""
        try:
            self._pebbleManager.connectToPebble(message.target) 
        except AttributeError as ae:
            print(ae)

    def _sendInstallCommand(self, message):
        """Install Pebble application"""
        self._pebbleManager.updatePebbleApp(message.target, message.data)

    def _sendNotification(self, message, note):
        """Send notification to Pebble"""
        self._pebbleManager.SendNotificationToPebble(message.target, note, message.uniqueID)