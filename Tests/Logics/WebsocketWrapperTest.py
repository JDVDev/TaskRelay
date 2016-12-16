import unittest
from mock import Mock, patch, MagicMock
from Logics.WebsocketWrapper import WebsocketWrapper

class Test_WebsocketWrapper(unittest.TestCase):
    @patch("websocket.WebSocketApp")
    @patch("Logics.WebsocketWrapper.WebsocketWrapper")
    def setUp(self, mock_ws_wrapper, mock_websocket):
        self.ws_wrapper = WebsocketWrapper()
        self.mock_ws_wrapper = mock_ws_wrapper
        self.mock_websocket = mock_websocket
        self.mock_url = Mock()
        self.mock_on_message = Mock()

    
    def test_WebsocketWrapper_01_Connect(self):
        self.mock_ws_wrapper.Connect(self.mock_url, self.mock_on_message)
        self.mock_ws_wrapper.Connect.assert_called_with(self.mock_url, self.mock_on_message)