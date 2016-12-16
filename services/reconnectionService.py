class reconnectionService():
    def __init__(self, pebble, message):
        self.targetPebble = pebble
    
    def reconnect(self):
        """Reconnect Pebble"""
        self.targetPebble.disconnect()
        self.targetPebble.connect()
        self.targetPebble.run_async()
        self.targetPebble.startAppMessageService()
        