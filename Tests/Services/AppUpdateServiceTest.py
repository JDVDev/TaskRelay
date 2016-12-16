import unittest
from mock import Mock, patch, mock_open

from services.AppUpdateService import AppUpdateService

class Test_appUpdateServiceTest(unittest.TestCase):
    def setUp(self):
        self.appUpdateService = AppUpdateService()

    @patch('builtins.open')
    @patch("Logics.RequestsWrapper.RequestsWrapper.get")
    def test_App_Update_Service_01_Download_App(self, mock_get, open_mock):
        url = Mock()
        self.appUpdateService.downloadApp(url)
        self.assertTrue(mock_get.called)

    @patch("libpebble2.services.install.AppInstaller.install")
    @patch("libpebble2.services.install.AppInstaller._prepare")
    @patch("Logics.AppInstallerWrapper.AppInstallerWrapper.install")
    @patch("Logics.AppInstallerWrapper.AppInstallerWrapper")
    def test_App_Update_Service_02_Install_App(self, mock_installer, mock_install, mock_prepare, mock_libpebble2_install):
        pebbleConnection = Mock()
        self.appUpdateService.installApp(pebbleConnection)

    @patch("services.AppUpdateService.AppUpdateService.installApp")
    @patch("services.AppUpdateService.AppUpdateService.downloadApp")
    def test_App_Update_Service_03_Update_Pebble_App(self, mock_download, mock_install):
        PebbleConnection = Mock()
        url = Mock()
        self.appUpdateService.updatePebbleApp(PebbleConnection, url)
        mock_download.assert_called_with(url)
        mock_install.assert_called_with(PebbleConnection)