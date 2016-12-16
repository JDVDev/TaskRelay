import unittest
from mock import Mock, patch
from services import AppStartService

class Test_openAppserviceTest(unittest.TestCase):
    def setUp(self):
        self.AppStartService = AppStartService.AppStartService

    @patch("services.AppStartService.AppStartService.openApp")
    def test_App_Open_Service_01_Open_App(self, mock_open_app):
        pebbleConnection = Mock()
        uuid = Mock()
        self.AppStartService.openApp(pebbleConnection, uuid)
        self.assertTrue(mock_open_app.called)
        mock_open_app.assert_called_with(pebbleConnection, uuid)