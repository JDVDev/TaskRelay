import unittest
from mock import Mock, patch
from Logics.AppInstallerWrapper import AppInstallerWrapper

class Test_AppInstallerWrapperTest(unittest.TestCase):
    @patch("libpebble2.services.install.AppInstaller._prepare")
    def setUp(self, mock_prepare):
        mock_connection = Mock()
        mock_file = Mock()
        self.appInstallerWrapper = AppInstallerWrapper(mock_connection, mock_file)

    @patch("libpebble2.services.install.AppInstaller.install")
    def test_01_AppInstallerWrapper_Install(self, mock_install):
        self.appInstallerWrapper.install()
        self.assertTrue(mock_install.called)
