import unittest
from mock import Mock, patch, MagicMock
from data import WebserviceURL

from Logics.WebsocketWrapper import WebsocketWrapper
from Logics.WebserviceClient import WebserviceClient

class Test_WebserviceClientTest(unittest.TestCase):
    @patch("Logics.WebserviceClient.WebserviceClient")
    @patch("Logics.WebsocketWrapper.WebsocketWrapper")
    def setUp(self, mock_ws_wrapper, mock_ws_client):
        self.mock_ws_wrapper = mock_ws_wrapper
        self.mock_ws_client = mock_ws_client
        self.mock_message_handler = Mock()
        self.ws_client = WebserviceClient(self.mock_ws_wrapper)
        self.mock_url = Mock()
        self.mock_on_message = Mock()

    def test_WebserviceClient_01_Connect_Parameters(self):
        self.mock_ws_client.connect(self.mock_message_handler)
        self.mock_ws_client.connect.assert_called_with(self.mock_message_handler)
    
    def test_WebserviceClient_02_Connect_Wrapper_Called_With_Right_Parameters(self):
        self.ws_client.Connect(self.mock_message_handler)
        self.assertTrue(self.mock_ws_wrapper.Connect.called)
        self.mock_ws_wrapper.Connect.assert_called_with(WebserviceURL.websocketUrl, self.mock_message_handler)