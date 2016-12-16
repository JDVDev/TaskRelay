import unittest
from services import serverMessageService
from mock import Mock, patch
from data import serverEnvelope

class Test_serverMessageServiceTest(unittest.TestCase):
    @patch("Logics.JSONWrapper.JSONWrapper")
    @patch("Logics.BluetoothManager.BluetoothManager")
    @patch("Logics.WebserviceClient.WebserviceClient")
    @patch("services.MessageMarshallerService.MessageMarshallerService")
    def setUp(self, mock_marshaller, mock_client, mock_bluetooth, mock_json_wrapper):
        self.serverMessageService = serverMessageService.serverMessageService(mock_marshaller, mock_client, mock_bluetooth, mock_json_wrapper)

    @patch("Logics.JSONWrapper.JSONWrapper.dumps")
    def test_01_encode_message(self, mock_json_dump):
        message = Mock()
        message.getAttributes.return_value = { "m", "s", "g" }
        self.serverMessageService._encodeMessageForServer(message)
        self.assertTrue(mock_json_dump.called)
        mock_json_dump.assert_called_with(message.getAttributes.return_value)





    @patch("Logics.BluetoothManager.BluetoothManager.sendAvailablePebblesToServer")
    def test_05_check_server_message_scan(self, mock_bluetooth_send):
        scanMessage = str(serverEnvelope.serverEnvelopeType.scan.value) + ','
        self.serverMessageService._checkServerMessage(scanMessage)
        self.assertTrue(mock_bluetooth_send.called)

    @patch("services.MessageMarshallerService.MessageMarshallerService.sendMessageToPebble")
    def test_06_check_server_message_connect(self, mock_send_to_pebble):
        connectMessage = str(serverEnvelope.serverEnvelopeType.connect.value) + ','
        self.serverMessageService._checkServerMessage(connectMessage)
        self.assertTrue(mock_send_to_pebble)
    
    @patch("Logics.WebserviceClient.WebserviceClient.send")
    @patch("services.MessageMarshallerService.MessageMarshallerService.sendMessageToPebble")
    def test_07_check_server_message_invalid(self, mock_send_to_pebble, mock_client_send):
        invalidMessage = ["i","n" ]
        self.serverMessageService._checkServerMessage(invalidMessage)
        self.assertFalse(mock_send_to_pebble.called)
        self.assertTrue(mock_client_send.called)