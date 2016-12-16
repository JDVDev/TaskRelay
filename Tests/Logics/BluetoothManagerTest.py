import unittest
from Logics import BluetoothManager
from mock import Mock, patch

class Test_BluetoothManagerTest(unittest.TestCase):
    @patch("services.OutgoingMessageService.OutgoingMessageService")
    def setUp(self, mock_message_service):
        self.bluetoothManager = BluetoothManager.BluetoothManager(mock_message_service)
        self.mock_message_service = mock_message_service

    @patch("subprocess.check_output")
    def test_BluetoothManager_01_Get_Paired_Pebbles(self, mock_subprocess):
        pebblePath = "'tty.Pebble4358-SerialPortSe'"
        mock_subprocess.return_value = pebblePath

        self.bluetoothManager._getPairedPebbles()
        self.assertTrue(mock_subprocess.called)

    def test_BluetoothManager_02_Get_Available_Pebbles(self):
        self.fail()

    def test_BluetoothManager_03_Check_Availability_Of_Paired_Pebbles(self):
        self.fail()

    @patch("Logics.BluetoothManager.BluetoothManager._checkAvailabilityOfPairedPebbles")
    @patch("Logics.BluetoothManager.BluetoothManager.getAvailablePebbles")
    @patch("Logics.BluetoothManager.BluetoothManager._getPairedPebbles")
    def test_BluetoothManager_04_Get_Available_Paired_Pebbles(self, mock_get , mock_scan, mock_check):
        availablePebbles = Mock()
        pairedPebbles = Mock()
        mock_get.return_value = pairedPebbles
        mock_scan.return_value = availablePebbles

        self.bluetoothManager.getAvailablePairedPebbles()

        self.assertTrue(mock_get.called)
        self.assertTrue(mock_scan.called)
        mock_check.assert_called_with(pairedPebbles, availablePebbles)

    @patch("Logics.BluetoothManager.BluetoothManager.getAvailablePairedPebbles")
    @patch("services.OutgoingMessageService.OutgoingMessageService.sendMessageToServer")
    def test_BluetoothManager_05_Send_Available_Pebbles_To_Server(self, mock_send, mock_get_pebbles):
        mock_pebbles = Mock()
        mock_get_pebbles.return_value = mock_pebbles
        self.bluetoothManager.sendAvailablePebblesToServer()
        self.assertTrue(mock_get_pebbles.called)

        self.mock_message_service.sendMessageToServer.assert_called_with(mock_pebbles)