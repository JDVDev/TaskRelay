from Logics.WebserviceClient import WebserviceClient
from Logics.JSONWrapper import JSONWrapper
from injector import inject, singleton

class OutgoingMessageService(object):
    @inject(jsonWrapper = JSONWrapper, webserviceClient = WebserviceClient)
    def __init__(self, jsonWrapper, webserviceClient):
        self._jsonWrapper = jsonWrapper
        self._webserviceClient = webserviceClient

    def _encodeMessageForServer(self, message):
        return self._jsonWrapper.dumps(message.getAttributes())
    
    def sendMessageToServer(self, message):
        """Send message to webservice and encode the message if necessary"""
        if type(message) is not str:
            message = self._encodeMessageForServer(message)
        self._webserviceClient.send(message)
