import json
from Logics.WebserviceClient import WebserviceClient
from services.IncomingMessageService import IncomingMessageService

from injector import inject, singleton


class MessagingService(object):
    @singleton
    @inject(webserviceClient = WebserviceClient, incomingMessageService = IncomingMessageService )
    def __init__(self, webserviceClient, incomingMessageService):
        self._webserviceClient = webserviceClient
        self._incomingMessageService = incomingMessageService
        self._errorMessage = "Invalid command"

    def ConnectToServer(self):
        self._webserviceClient.Connect(self._messageHandler)

    def _messageHandler(self, socket, message):
        """Handle incoming web message""""
        self._readMessageFromServer(message)  
    
    def _readMessageFromServer(self, message):
        if self._incomingMessageService.HandleIncomingMessage(message) == False:
            self._webserviceClient.send(self._errorMessage)