import subprocess
import bluetooth
from data import PebbleEnvelope
from services.OutgoingMessageService import OutgoingMessageService
from injector import inject

class BluetoothManager():  
    @inject(outgoingMessageService = OutgoingMessageService)
    def __init__(self, outgoingMessageService):
        self._outgoingMessageService = outgoingMessageService

    def _getPairedPebbles(self):
        """Execute linux shell command to get paired Pebbles"""
        pairedPebbles = str(subprocess.check_output("ls /dev/ | grep tty.Pebble", shell=True))
        pairedPebbles = pairedPebbles.replace("tty.", "")
        pairedPebbles = pairedPebbles.replace("b'", "")
        pairedDevices = pairedPebbles.split("-SerialPortSe\\n")     
        pairedDevices.remove("'")  
        return pairedDevices 

    def getAvailablePebbles(self):
        """Scan for available Pebbles"""
        available = []
        availablePebbles = []
        availableDevices = bluetooth.discover_devices(lookup_names = True) 
        for addr,name in availableDevices:
            if 'Pebble' in name: available.append(name)
        for pebble in available: 
            pebbleName = pebble.replace(" ", "")
            availablePebbles.append(pebbleName)
        return availablePebbles
    
    def _checkAvailabilityOfPairedPebbles(self, pairedPebbles, availablePebbles):
        """Check which available Pebbles are already paired"""
        return list((set(pairedPebbles) & set(availablePebbles)))

    def getAvailablePairedPebbles(self):
        pairedDevices = self._getPairedPebbles()
        availablePebbles = self.getAvailablePebbles()
        availablePairedPebbles = self._checkAvailabilityOfPairedPebbles(pairedDevices, availablePebbles)
        return PebbleEnvelope.pebbleListEnvelope(availablePairedPebbles);

    def sendAvailablePebblesToServer(self):
        """Notify webservice of available Pebbles"""
        availablePairedList = self.getAvailablePairedPebbles()
        self._outgoingMessageService.sendMessageToServer(availablePairedList)