from libpebble2.services.install import AppInstaller

class AppInstallerWrapper():
    """Wrapper used for unit testing"""
    def __init__(self, PebbleConnection, AppFileName):
        self.pebbleConnection = PebbleConnection
        self.appFileName = AppFileName
        self.installer = AppInstaller(PebbleConnection, "pebbleApp.pbw")
    
    def install(self):
        self.installer.install()
