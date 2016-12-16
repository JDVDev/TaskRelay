from services.MessagingService import MessagingService 
from Logics.WebserviceClient import WebserviceClient
from Logics.BluetoothManager import BluetoothManager
from Logics.PebbleManager import PebbleManager

from services.IncomingMessageService import IncomingMessageService
from services.IncomingPebbleMessageService import IncomingPebbleMessageService
from services.OutgoingMessageService import OutgoingMessageService
from services.OutgoingPebbleMessageService import OutgoingPebbleMessageService
from services.MessagingService import MessagingService


Singletons = [
    WebserviceClient, 
    MessagingService,
    BluetoothManager,
    PebbleManager,
    IncomingMessageService,
    IncomingPebbleMessageService,
    OutgoingMessageService,
    OutgoingPebbleMessageService
    ]