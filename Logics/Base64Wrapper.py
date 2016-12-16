import base64

class Base64Wrapper():
    """Wrapper used for unit testing"""
    def encode(self, data):
        encoded = data.encode('utf-8')
        print("utf-8 encoded")
        bencoded = base64.b64encode(encoded)
        print("base64 encoded")
        return bencoded
