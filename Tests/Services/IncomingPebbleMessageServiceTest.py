import unittest
from mock import Mock, patch
from services.IncomingPebbleMessageService import IncomingPebbleMessageService
from data import ServerEnvelope

class Test_IncomingPebbleMessageServiceTest(unittest.TestCase):
    @patch("Logics.PebbleManager.PebbleManager")
    def setUp(self, mock_manager):
        self.incomingPebbleMessageService = IncomingPebbleMessageService(mock_manager) 
        self.mock_manager = mock_manager

    @patch("services.IncomingPebbleMessageService.IncomingPebbleMessageService._sendAppMessageToPebble")
    @patch("Logics.WebserviceClient.WebserviceClient.send")
    def test_IncomingPebbleMessageService_01_Send_Message_To_Pebble_App_Message(self, mock_client_send, mock_send_appmsg):
        appMessage = Mock()
        appMessage.envelopeType = ServerEnvelope.ServerEnvelopeType.message.value
        self.incomingPebbleMessageService.sendMessageToPebble(appMessage)
        self.assertTrue(mock_send_appmsg.called)
        mock_send_appmsg.assert_called_with(appMessage)

    @patch("services.IncomingPebbleMessageService.IncomingPebbleMessageService._sendDisconnectCommand")
    def test_IncomingPebbleMessageService_02_Send_Message_To_Pebble_Disconnect(self, mock_disconnect):
        disconnectMessage = Mock()
        disconnectMessage.envelopeType = ServerEnvelope.ServerEnvelopeType.disconnect.value
        self.incomingPebbleMessageService.sendMessageToPebble(disconnectMessage)
        self.assertTrue(mock_disconnect.called)
        mock_disconnect.assert_called_with(disconnectMessage)

    @patch("services.IncomingPebbleMessageService.IncomingPebbleMessageService._sendConnectCommand")
    def test_IncomingPebbleMessageService_03_Send_Message_To_Pebble_Connect(self, mock_connect):
        connectMessage = Mock()
        connectMessage.envelopeType = ServerEnvelope.ServerEnvelopeType.connect.value
        self.incomingPebbleMessageService.sendMessageToPebble(connectMessage)
        self.assertTrue(mock_connect.called)
        mock_connect.assert_called_with(connectMessage)

    @patch("services.IncomingPebbleMessageService.IncomingPebbleMessageService._sendInstallCommand")
    def test_IncomingPebbleMessageService_04_Send_Message_To_Pebble_Install(self, mock_install):
        installMessage = Mock()
        installMessage.envelopeType = ServerEnvelope.ServerEnvelopeType.install.value
        self.incomingPebbleMessageService.sendMessageToPebble(installMessage)
        self.assertTrue(mock_install.called)
        mock_install.assert_called_with(installMessage)

    def test_IncomingPebbleMessageService_05_Check_Availability_Of_Pebble(self):
        pebbleAddress = Mock()
        self.incomingPebbleMessageService._checkAvailabilityOfPebble(pebbleAddress)
        self.assertTrue(self.mock_manager._getPebble.called)
        self.mock_manager._getPebble.assert_called_with(pebbleAddress)

    @patch("Pebble.Pebble")
    def test_IncomingPebbleMessageService_06_Send_AppMessage_To_Pebble(self, mock_pebble):
        message = Mock()
        self.mock_manager._getPebble.return_value = mock_pebble
        self.incomingPebbleMessageService._sendAppMessageToPebble(message)
        self.assertTrue(self.mock_manager._getPebble.called)
        self.mock_manager._getPebble.assert_called_with(message.target)
        self.assertTrue(mock_pebble.sendAppMessage.called)

    def test_IncomingPebbleMessageService_07_Send_Disconnect_command(self):
        disconnectMessage = Mock()
        self.incomingPebbleMessageService._sendDisconnectCommand(disconnectMessage)
        self.assertTrue(self.mock_manager.disconnectFromPebble.called)
        self.mock_manager.disconnectFromPebble.assert_called_with(disconnectMessage.target)

    def test_IncomingPebbleMessageService_08_Send_Connect_Command(self):
        connectMessage = Mock()
        self.incomingPebbleMessageService._sendConnectCommand(connectMessage)
        self.assertTrue(self.mock_manager.connectToPebble.called)
        self.mock_manager.connectToPebble.assert_called_with(connectMessage.target)

    def test_IncomingPebbleMessageService_09_Send_Install_Command(self):
        installMessage = Mock()
        self.incomingPebbleMessageService._sendInstallCommand(installMessage)
        self.assertTrue(self.mock_manager.updatePebbleApp.called)