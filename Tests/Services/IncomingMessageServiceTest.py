import unittest
from mock import Mock, patch, MagicMock
from services.IncomingMessageService import IncomingMessageService
from data import ServerEnvelope, PebbleCommand


class Test_IncomingMessageServiceTest(unittest.TestCase):
    @patch("services.IncomingPebbleMessageService.IncomingPebbleMessageService")
    @patch("Logics.BluetoothManager.BluetoothManager")
    def setUp(self, mock_bluetooth_manager, mock_pebble_service):
        self.incomingMsgService = IncomingMessageService(mock_bluetooth_manager, mock_pebble_service)
        self.mock_pebble_service = mock_pebble_service
        self.mock_bluetooth_manager = mock_bluetooth_manager

    @patch("services.IncomingMessageService.IncomingMessageService._readMessageFromServer")
    def test_IncomingMessageService_01_Message_Handler_Read_Called(self, readMessage):
        mock_socket = Mock()
        message = "1,Pebble623D"
        self.incomingMsgService.HandleIncomingMessage(message)
        self.assertTrue(readMessage.called)
        readMessage.assert_called_with(message)
    
    @patch("Logics.WebserviceClient.WebserviceClient.send")
    @patch("Pebble.Pebble.connect")
    @patch("services.IncomingMessageService.IncomingMessageService._checkServerMessage")   
    def test_IncomingMessageService_02_Read_Message_From_Server(self, mock_check_msg, mock_connect, mock_client_send):
        message = "1,2,3,4,5"
        splittedMessage = message.split(',')
        splittedMessage = list(filter(None, splittedMessage))
        self.incomingMsgService._readMessageFromServer(message)
        self.assertTrue(mock_check_msg.called)
        mock_check_msg.assert_called_with(splittedMessage)

    @patch("Logics.WebserviceClient.WebserviceClient.send")
    @patch("services.IncomingPebbleMessageService.IncomingPebbleMessageService.sendMessageToPebble")
    def test_IncomingMessageService_03_Check_Server_Message_Invalid(self, mock_send_to_pebble, mock_client_send):
        invalidMessage = ["9","n" ]
        self.incomingMsgService._checkServerMessage(invalidMessage)
        self.assertFalse(mock_send_to_pebble.called)
    
    @patch("services.IncomingMessageService.IncomingMessageService._HandleConnectionCommand")
    def test_IncomingMessageService_04_Check_Server_Message_Connect(self, mock_connect):
        connectMessage = [None] * 2
        envelopeType = ServerEnvelope.ServerEnvelopeType.connect.value
        targetPebble = Mock()
        connectMessage[0] = envelopeType
        connectMessage[1] = targetPebble
        self.incomingMsgService._checkServerMessage(connectMessage)
        self.assertTrue(mock_connect.called)
        mock_connect.assert_called_with(envelopeType, targetPebble)
        self.assertTrue(self.mock_pebble_service.sendMessageToPebble.called)
    
    @patch("services.IncomingMessageService.IncomingMessageService._HandleConnectionCommand")  
    def test_IncomingMessageService_05_Check_Server_Message_Disconnect(self, mock_connect):
        disconnectMessage = [None] * 2
        envelopeType = ServerEnvelope.ServerEnvelopeType.disconnect.value
        targetPebble = Mock()
        disconnectMessage[0] = envelopeType
        disconnectMessage[1] = targetPebble
        self.incomingMsgService._checkServerMessage(disconnectMessage)
        self.assertTrue(mock_connect.called)
        mock_connect.assert_called_with(envelopeType, targetPebble)
        self.assertTrue(self.mock_pebble_service.sendMessageToPebble.called)

    @patch("services.IncomingMessageService.IncomingMessageService._HandleMessagingCommand")  
    def test_IncomingMessageService_06_Check_Server_Message_Msg(self, mock_handle_message):
        message = str(ServerEnvelope.ServerEnvelopeType.message.value) + ',Pebble623D,,'
        self.incomingMsgService._checkServerMessage(message)
        self.assertTrue(mock_handle_message.called)
        mock_handle_message.assert_called_with(message)
        self.assertTrue(self.mock_pebble_service.sendMessageToPebble.called)

    @patch("services.IncomingMessageService.IncomingMessageService._HandleScanCommand")  
    @patch("Logics.BluetoothManager.BluetoothManager.getAvailablePairedPebbles")
    def test_IncomingMessageService_07_Check_Server_Message_Scan(self, get_pebbles, mock_handle_scan):
        scanMessage = str(ServerEnvelope.ServerEnvelopeType.scan.value) + ",Pebble623D"
        mock_pebbles = Mock()
        get_pebbles.return_value = mock_pebbles
        self.incomingMsgService._checkServerMessage(scanMessage)
        self.assertTrue(mock_handle_scan.called)

    @patch("services.IncomingMessageService.IncomingMessageService._HandleInstallCommand")  
    def test_IncomingMessageService_08_Check_Server_Message_Install(self, mock_install):
        installMessage = [None] * 3
        messageType = str(ServerEnvelope.ServerEnvelopeType.install.value)
        targetPebble = Mock()
        url = Mock()
        installMessage[0] = messageType
        installMessage[1] = targetPebble
        installMessage[2] = url
        self.incomingMsgService._checkServerMessage(installMessage)
        self.assertTrue(mock_install.called)
        mock_install.assert_called_with(targetPebble, url)
        self.assertTrue(self.mock_pebble_service.sendMessageToPebble.called)

    @patch("services.IncomingMessageService.IncomingMessageService._HandleNotificationCommand")  
    def test_IncomingMessageService_09_Check_Server_Message_Notification(self, mock_handle_notification):
        notificationMessage = [None] * 3
        targetPebble = Mock()
        notification = Mock()
        notificationMessage[0] = ServerEnvelope.ServerEnvelopeType.notification.value
        notificationMessage[1] = targetPebble
        notificationMessage[2] = notification      
       
        self.incomingMsgService._checkServerMessage(notificationMessage)
        self.assertTrue(mock_handle_notification.called)
        mock_handle_notification.assert_called_with(targetPebble, notification)

    @patch("Logics.BluetoothManager.BluetoothManager.sendAvailablePebblesToServer")
    def test_IncomingMessageService_10_Handle_Scan_Command(self, mock_send):
        self.incomingMsgService._HandleScanCommand()
        self.assertTrue(self.mock_bluetooth_manager.sendAvailablePebblesToServer.called)