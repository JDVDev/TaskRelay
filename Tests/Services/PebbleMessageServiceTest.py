import unittest
from mock import Mock, patch
from services import PebbleMessageService
from data import serverEnvelope

class Test_PebbleMessageServiceTest(unittest.TestCase):
    @patch("Logics.PebbleManager.PebbleManager")
    @patch("services.MessageMarshallerService.MessageMarshallerService")
    def setUp(self, mock_marshaller, mock_manager):
        self.pebbleMessageService = PebbleMessageService.PebbleMessageService(mock_marshaller, mock_manager) 



    @patch("services.PebbleMessageService.PebbleMessageService._sendAppMessageToPebble")
    @patch("Logics.WebserviceClient.WebserviceClient.send")
    def test_PebbleMessageService_02_Send_Message_To_Pebble_App_Message(self, mock_client_send, mock_send_appmsg):
        appMessage = Mock()
        appMessage.envelopeType = serverEnvelope.serverEnvelopeType.message.value
        self.pebbleMessageService.sendMessageToPebble(appMessage)
        self.assertTrue(mock_send_appmsg.called)
        mock_send_appmsg.assert_called_with(appMessage)

    @patch("services.PebbleMessageService.PebbleMessageService._sendDisconnectCommand")
    def test_PebbleMessageService_03_Send_Message_To_Pebble_Disconnect(self, mock_disconnect):
        disconnectMessage = Mock()
        disconnectMessage.envelopeType = serverEnvelope.serverEnvelopeType.disconnect.value
        self.pebbleMessageService.sendMessageToPebble(disconnectMessage)
        self.assertTrue(mock_disconnect.called)
        mock_disconnect.assert_called_with(disconnectMessage)

    @patch("services.PebbleMessageService.PebbleMessageService._sendConnectCommand")
    def test_PebbleMessageService_04_Send_Message_To_Pebble_Connect(self, mock_connect):
        connectMessage = Mock()
        connectMessage.envelopeType = serverEnvelope.serverEnvelopeType.connect.value
        self.pebbleMessageService.sendMessageToPebble(connectMessage)
        self.assertTrue(mock_connect.called)
        mock_connect.assert_called_with(connectMessage)