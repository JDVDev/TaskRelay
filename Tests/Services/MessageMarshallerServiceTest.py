import unittest
from mock import Mock, patch
from services.MessageMarshallerService import MessageMarshallerService

class Test_MessageMarshallerServiceTest(unittest.TestCase):
    @patch("services.MessagingService.MessagingService")
    @patch("services.PebbleMessageService.PebbleMessageService")
    def setUp(self, mock_pebble_message_service, mock_messaging_service):
        self.messageMarshallerService = MessageMarshallerService(mock_pebble_message_service, mock_messaging_service)
       
    @patch("Logics.WebserviceClient.WebserviceClient.send")
    @patch("Logics.JSONWrapper.JSONWrapper.dumps")
    @patch("services.MessagingService.MessagingService.sendMessageToServer")
    def test_MessageMarshallerService_01_Send_Message_To_Server(self, mock_send_message_to_server, mock_json, mock_send):
        message = Mock()
        self.messageMarshallerService.sendMessageToServer(message)
        self.assertTrue(mock_send_message_to_server.called)
        mock_send_message_to_server.assert_called_with(message)

    @patch("services.PebbleMessageService.PebbleMessageService.sendMessageToPebble")
    def test_MessageMarshallerService_02_Send_Message_To_Pebble(self, mock_send_message_to_pebble):
        message = Mock()
        self.messageMarshallerService.sendMessageToPebble(message)
        self.assertTrue(mock_send_message_to_pebble.called)
        mock_send_message_to_pebble.assert_called_with(message)