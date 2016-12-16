import time
from threading import Timer
from data.PebbleStatus import PebbleStatus
from data.DeliveryStatus import DeliveryStatus
import copy
from services.OutgoingPebbleMessageService import OutgoingPebbleMessageService
from factories.PebbleFactory import PebbleFactory
from services.AppUpdateService import AppUpdateService
from injector import inject, singleton


from libpebble2.services.notifications import Notifications

class PebbleManager():
    @singleton
    @inject(outgoingPebbleMessageService = OutgoingPebbleMessageService, pebbleFactory = PebbleFactory, appUpdateService = AppUpdateService)
    def __init__(self, outgoingPebbleMessageService, pebbleFactory, appUpdateService):
        self._outgoingPebbleMessageService = outgoingPebbleMessageService
        self._pebbleFactory = pebbleFactory
        self._appUpdateService = appUpdateService
        self._pebbleDict = {}
        self._disconnectedPebbles = {}
    
    def _registerPebble(self, pebble):
        """Register connected Pebble and notify webservice"""
        self._pebbleDict[pebble.name] = pebble
        self._outgoingPebbleMessageService.sendStatusToMarshaller(pebble.name, PebbleStatus.connected.value)
        
    def _unregisterPebble(self, pebble):
        """Register disconnected Pebble and notify webservice"""
        try:
            del self._pebbleDict[pebble.name]
        except KeyError:
            pass
        self._disconnectedPebbles[pebble.name] = pebble
        self._outgoingPebbleMessageService.sendStatusToMarshaller(pebble.name, PebbleStatus.disconnected.value)

    def _getPebble(self, pebbleAddress):
        """Get registered Pebble by address"""
        try:
            return self._pebbleDict[pebbleAddress]
        except KeyError:
            try:
                return self._disconnectedPebbles[pebbleAddress]
            except KeyError:
                pass
    
    def connectToPebble(self, pebbleAddress):
        """Connect to given Pebble"""
        newPebble = self._pebbleFactory.producePebble(pebbleAddress)
        if(newPebble.connect()):
            self._registerPebble(newPebble)
        else:
            self._outgoingPebbleMessageService.sendStatusToMarshaller(newPebble.name, PebbleStatus.failed.value)

    def disconnectFromPebble(self, pebbleAddress):
        """Disconnect from given Pebble"""
        print("disconnecting")
        targetPebble = self._getPebble(pebbleAddress)
        targetPebble.disconnect()
        print("disconnected>")
        self._unregisterPebble(targetPebble)

    def disconnectAllPebbles(self):
        """Disconnect all Pebbles and notify webservice"""
        for pebbleName in self._pebbleDict:
            self._pebbleDict[pebbleName].pebbleConnection.transport.connection.close() 
            self._outgoingPebbleMessageService.sendStatusToMarshaller(pebbleName, PebbleStatus.disconnected.value)

    def updatePebbleApp(self, targetPebble, url):
        """Update Pebble Application"""
        print("update")
        if not self._appUpdateService.updatePebbleApp((self._getPebble(targetPebble).pebbleConnection), url):
            print("install failed")

    def SendNotificationToPebble(self, target, message, transactionId):
        """Send notification to Pebble"""
        print("send note: " + message)
        if(type(target) == str): target = self._getPebble(target)
        note = Notifications(target.pebbleConnection)
        try:
            note.send_notification(message = message)
        except:
            self._outgoingPebbleMessageService.sendDeliveryStatusToMarshaller(transactionId, DeliveryStatus.NACK.value)
