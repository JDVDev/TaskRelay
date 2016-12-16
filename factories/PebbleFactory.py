import Pebble
from .PebbleConnectionFactory import PebbleConnectionFactory
from .MessageServiceFactory import MessageServiceFactory
from services.AppStartService import AppStartService
from services.OutgoingPebbleMessageService import OutgoingPebbleMessageService 
from injector import inject, singleton
from Logics.BluetoothManager import BluetoothManager

class PebbleFactory():
    @singleton
    @inject(bluetoothManager = BluetoothManager, pebbleConnectionFactory = PebbleConnectionFactory, messageServiceFactory = MessageServiceFactory, appStartService = AppStartService, outgoingPebbleMessageService = OutgoingPebbleMessageService)
    def __init__(self, bluetoothManager, pebbleConnectionFactory, messageServiceFactory, appStartService, outgoingPebbleMessageService ):
        self._bluetoothManager = bluetoothManager
        self._connectionFactory = pebbleConnectionFactory
        self._messageFactory = messageServiceFactory
        self._appStartService = appStartService
        self._outgoingPebbleMessageService = outgoingPebbleMessageService
   
    def producePebble(self, pebbleName):
        return Pebble.Pebble(pebbleName, self._connectionFactory, self._messageFactory, self._appStartService, self._outgoingPebbleMessageService)


