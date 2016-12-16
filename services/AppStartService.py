from Logics.AppStartServiceWrapper import AppStartServiceWrapper
from injector import inject

class AppStartService():
    @inject(appStartMessageService = AppStartServiceWrapper)
    def __init__(self, appStartMessageService):
        self._appStartServiceWrapper = appStartMessageService

    def openApp(self, pebbleConnection, uuid ):
        """Open pebble application with given UUID on given pebble"""
        self._appStartServiceWrapper.openApp(pebbleConnection, uuid )