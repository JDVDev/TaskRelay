from libpebble2.communication.transports.serial import SerialTransport
from libpebble2.communication import PebbleConnection

class PebbleConnectionFactory():
    @staticmethod
    def produceSerial(name):
        return PebbleConnection(SerialTransport("/dev/tty." + name + "-SerialPortSe"))