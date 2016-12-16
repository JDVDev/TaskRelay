from injector import Injector, inject, singleton
from services.MessagingService import MessagingService 
from Logics.WebserviceClient import WebserviceClient
from Logics.BluetoothManager import BluetoothManager
from Logics.PebbleManager import PebbleManager

from services.IncomingMessageService import IncomingMessageService
from services.IncomingPebbleMessageService import IncomingPebbleMessageService

from data.Singletons import Singletons

import sys

class Bootstrapper():
    def __init__(self):
        self._injector = None

    def singletons(self, binder):
        for s in Singletons:
            binder.bind(s, scope=singleton)

    def start_routine(self):
        self._injector = Injector([self.singletons])
        messagingService = self._injector.get(MessagingService)
        messagingService.ConnectToServer()    

    def stop_routine(self):
        pebbleManager = self._injector.get(PebbleManager)
        pebbleManager.disconnectAllPebbles()
        sys.exit(0)
        
bootstrapper = Bootstrapper()
bootstrapper.start_routine()

