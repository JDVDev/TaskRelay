from Logics.WebsocketWrapper import WebsocketWrapper
from Logics.Base64Wrapper import Base64Wrapper
from data import WebserviceURL
from injector import inject, singleton, Module


class WebserviceClient(object):
    @inject(websocket_wrapper = WebsocketWrapper, base64_wrapper = Base64Wrapper)
    def __init__(self, websocket_wrapper, base64_wrapper):
        self._webSocketWrapper = websocket_wrapper
        self._base64Wrapper = base64_wrapper
        self._socketConnection = None

    def Connect(self, messageHandler, timeout = None):
        print("Connecting")
        try:
            self._socketConnection = self._webSocketWrapper.Connect(WebserviceURL.websocketUrl, messageHandler, 'Basic b3dlbjpHcmFhZmxhbmQxOGE=', self.errorHandler)
            print("socket created")
            self._socketConnection.run_forever()
            return True
        except Exception as socketError:
#           clss.Connect(timeout)
            print(socketError)
            print("client closed")
            return False

    def errorHandler(self,ws,error):
        print(error)

    def send(self, message):
        if not self._socketConnection:
            raise Exception("Not yet connected to service")

        self._socketConnection.send(message)
