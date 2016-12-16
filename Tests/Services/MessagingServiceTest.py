import unittest
from mock import Mock, patch, MagicMock
from services.MessagingService import MessagingService

class Test_MessagingServiceTest(unittest.TestCase):
    @patch("Logics.WebserviceClient.WebserviceClient")
    @patch("services.IncomingMessageService.IncomingMessageService")
    def setUp(self, mock_message_service, mock_client):
        self.msgService = MessagingService(mock_client, mock_message_service)
        self.mock_client = mock_client
        self.mock_incoming_msg_service = mock_message_service

    def test_MessagingService_01_Connect_To_Server(self):
        self.msgService.ConnectToServer()
        self.assertTrue(self.mock_client.Connect.called)
    
    def test_MessagingService_02_Connect_Called_With_Handler(self):
        self.msgService.ConnectToServer()
        self.mock_client.Connect.assert_called_with(self.msgService._messageHandler)

    @patch("Logics.WebserviceClient.WebserviceClient.send")
    def test_MessagingService_03_Read_Message_From_Server(self, mock_client_send):
        message = Mock()
        self.mock_incoming_msg_service.HandleIncomingMessage.return_value = True
        self.msgService._readMessageFromServer(message)
        self.assertTrue(self.mock_incoming_msg_service.HandleIncomingMessage.called)
        self.mock_incoming_msg_service.HandleIncomingMessage.assert_called_with(message)
        
        self.mock_incoming_msg_service.HandleIncomingMessage.return_value = False
        self.msgService._readMessageFromServer(message)
        self.assertTrue(self.mock_client.send.called)
