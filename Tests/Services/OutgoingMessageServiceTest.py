import unittest
from mock import Mock, patch
from services.OutgoingMessageService import OutgoingMessageService
class Test_OutgoingMessageServiceTest(unittest.TestCase):
    
    @patch("Logics.JSONWrapper.JSONWrapper")
    @patch("Logics.WebserviceClient.WebserviceClient")
    def setUp(self, mock_client, mock_json_wrapper):
        self.outGoingMsgService = OutgoingMessageService(mock_json_wrapper, mock_client)
        self.mock_json_wrapper = mock_json_wrapper
        self.mock_client = mock_client

    def test_OutgoingMessageService_01_Encode_Message(self):
        message = Mock()
        message.getAttributes.return_value = { "m", "s", "g" }
        self.outGoingMsgService._encodeMessageForServer(message)
        self.assertTrue(self.mock_json_wrapper.dumps.called)
        self.mock_json_wrapper.dumps.assert_called_with(message.getAttributes.return_value)

    def test_OutgoingMessageService_02_Send_Message_To_Server_String(self):
        strMessage = "message"
        self.outGoingMsgService.sendMessageToServer(strMessage)
        self.assertTrue(self.mock_client.send.called)
        self.mock_client.send.assert_called_with(strMessage)

    @patch("Logics.WebserviceClient.WebserviceClient.send")
    @patch("services.OutgoingMessageService.OutgoingMessageService._encodeMessageForServer")   
    def test_OutgoingMessageService_03_Send_Message_To_Server_Dict(self, mock_encode, mock_send):
        dictMessage = { "m", "s", "g" }
        self.outGoingMsgService.sendMessageToServer(dictMessage)
        self.assertTrue(mock_encode.called)
        mock_encode.assert_called_with(dictMessage)