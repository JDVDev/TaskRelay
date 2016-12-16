from libpebble2.services.appmessage import AppMessageService
from libpebble2.protocol.legacy2 import LegacyAppLaunchMessage
from libpebble2.services.appmessage import Uint8
from libpebble2.communication import PebbleConnection

class AppStartServiceWrapper():
    """Wrapper used for unit testing"""
    def __init__(self):
        pass

    def openApp(self, pebbleConnection, uuid ):
        AppStartService = AppMessageService(pebbleConnection, message_type=LegacyAppLaunchMessage)
        AppStartService.send_message(uuid, {
            LegacyAppLaunchMessage.Keys.RunState: Uint8(LegacyAppLaunchMessage.States.Running)
        })
        AppStartService.shutdown()
        