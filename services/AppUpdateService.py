from Logics import RequestsWrapper
import subprocess
from Logics.AppInstallerWrapper import AppInstallerWrapper

class AppUpdateService():
    def __init__(self):
        pass

    def downloadApp(self, url):
        """Download pebble application from given URL"""
        try:
            b = RequestsWrapper.RequestsWrapper.get(url)
        except:
            print("invalid URL:" + url + "!")
            return False
        with open("pebbleApp.pbw", "wb") as app:
            app.write(b.content)
            return True
    
    def installApp(self, PebbleConnection):
        """Install downloaded pebble application"""
        installer = AppInstallerWrapper(PebbleConnection, "pebbleApp.pbw")
        installer.install()
    
    def updatePebbleApp(self, PebbleConnection, url):
        if(self.downloadApp(url)):
            self.installApp(PebbleConnection)
            return True
        return False
