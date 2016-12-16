import websocket
import base64
class WebsocketWrapper():
    """Wrapper used for unit testing"""
	def Connect(self, url, onMessage, authenticationHeader, errorHandler):
		return websocket.WebSocketApp(url, on_message=onMessage, header = { 'Authorization' : authenticationHeader }, on_error = errorHandler)
