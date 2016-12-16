from libpebble2.services.appmessage import AppMessageService
from libpebble2.services.appmessage import CString
from datetime import datetime

class MessageServiceFactory():
    @staticmethod
    def produceAppMessageService(pebbleConnection):
        return AppMessageService(pebbleConnection)
    @staticmethod
    def produceAppMessage(type, message, uniqueID = "", itemList = None):
        if(type == 0):
            return {int(type): CString(message),3: CString(str(uniqueID))}
        if(type == 2):
            currentTime = datetime.now()
            return {int(type): CString(message),3: CString(str(uniqueID)), 4: CString(str(currentTime.hour)) , 5: CString(str(currentTime.minute)), 6: CString(str(currentTime.second)) }
        return {int(type): CString(message),2: CString(str(uniqueID)),3: CString(itemList) }
        
