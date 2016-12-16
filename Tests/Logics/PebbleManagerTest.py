import unittest
from Logics.PebbleManager import PebbleManager
from mock import Mock, patch
from data.PebbleStatus import PebbleStatus

class Test_PebbleManagerTest(unittest.TestCase):
    @patch("Pebble.Pebble")
    @patch("services.AppUpdateService.AppUpdateService")
    @patch("factories.PebbleFactory.PebbleFactory")
    @patch("services.OutgoingPebbleMessageService.OutgoingPebbleMessageService")
    def setUp(self, mock_pebble_service, mock_pebble_factory, mock_update, mock_pebble ):
        self.pebbleManager = PebbleManager(mock_pebble_service, mock_pebble_factory, mock_update)
        self.mock_pebble = mock_pebble
        self.mock_pebble.name = "Pebble623D"
        self.mock_pebble._getPebble.return_value = mock_pebble
        self.mock_pebble_service = mock_pebble_service
        self.mock_pebble_factory = mock_pebble_factory
        self.mock_update = mock_update

    def test_PebbleManager_01_Register_Pebble_Update_Status_Called(self):
        self.pebbleManager._registerPebble(self.mock_pebble)
        self.assertTrue(self.mock_pebble_service.sendStatusToMarshaller.called)
        self.mock_pebble_service.sendStatusToMarshaller.assert_called_with(self.mock_pebble.name, PebbleStatus.connected.value)     
        self.assertTrue(len(self.pebbleManager._pebbleDict) == 1)

    @patch("services.OutgoingPebbleMessageService.OutgoingPebbleMessageService.sendStatusToMarshaller")
    def test_PebbleManager_02_Unregister_Pebble(self, mock_send_status):
        self.pebbleManager._unregisterPebble(self.mock_pebble)
        self.assertTrue(self.mock_pebble_service.sendStatusToMarshaller.called)
        self.mock_pebble_service.sendStatusToMarshaller.assert_called_with(self.mock_pebble.name, PebbleStatus.disconnected.value)     
        self.assertTrue(len(self.pebbleManager._disconnectedPebbles) == 1)

    @patch("Logics.PebbleManager.PebbleManager._getPebble")
    def test_PebbleManager_03_Get_Pebble(self, mock_get):
        self.pebbleManager._getPebble(self.mock_pebble.name)
        mock_get.assert_called_with(self.mock_pebble.name)

    @patch("Logics.WebserviceClient.WebserviceClient.send")
    def test_PebbleManager_04_Connect_To_Pebble(self, mock_send):
        self.mock_pebble_factory.producePebble.return_value = self.mock_pebble
        self.pebbleManager.connectToPebble(self.mock_pebble.name)
        self.assertTrue(self.mock_pebble_factory.producePebble.called)
        self.mock_pebble_factory.producePebble.assert_called_with(self.mock_pebble.name)
        self.assertTrue(self.mock_pebble.connect.called)

    @patch("Logics.JSONWrapper.JSONWrapper.dumps")
    @patch("Logics.WebserviceClient.WebserviceClient.send")
    @patch("Logics.PebbleManager.PebbleManager._getPebble")
    def test_PebbleManager_05_Disconnect_From_Pebble(self, mock_get, mock_produce, mock_json):
        mock_get.return_value = self.mock_pebble
        self.pebbleManager.disconnectFromPebble(self.mock_pebble.name)
        self.assertTrue(mock_get.called)
        self.assertTrue(self.mock_pebble.disconnect.called)


    def test_PebbleManager_06_Disconnect_All_Pebbles(self):
        self.pebbleManager._pebbleDict[self.mock_pebble.name] = self.mock_pebble
        self.pebbleManager.disconnectAllPebbles()
        self.assertTrue(self.mock_pebble_service.sendStatusToMarshaller.called)
        self.mock_pebble_service.sendStatusToMarshaller.assert_called_with(self.mock_pebble.name,PebbleStatus.disconnected.value)

    @patch("services.AppUpdateService.AppUpdateService.updatePebbleApp")
    def test_PebbleManager_07_Update_Pebble_App(self, mock_update_app):
        url = Mock()
        self.pebbleManager._pebbleDict[self.mock_pebble.name] = self.mock_pebble
        self.pebbleManager.updatePebbleApp(self.mock_pebble.name, url)
        self.assertTrue(self.mock_update.updatePebbleApp.called)