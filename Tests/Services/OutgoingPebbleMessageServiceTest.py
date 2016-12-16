import unittest
from services.OutgoingPebbleMessageService import OutgoingPebbleMessageService
from mock import Mock, patch
from data import PebbleEnvelope


class Test_OutgoingPebbleMessageServiceTest(unittest.TestCase):
    @patch("services.OutgoingMessageService.OutgoingMessageService")
    def setUp(self, mock_msg_service):
        self.outgoingPebbleMessageService = OutgoingPebbleMessageService(mock_msg_service)
        self.mock_msg_service = mock_msg_service

    def test_PebbleMessageService_01_Send_Message_To_Marshaller(self):
        message = Mock()
        self.outgoingPebbleMessageService.sendMessageToMarshaller(message)
        self.assertTrue(self.mock_msg_service.sendMessageToServer.called)
        self.mock_msg_service.sendMessageToServer.assert_called_with(message)

    @patch("services.OutgoingPebbleMessageService.OutgoingPebbleMessageService.sendStatusToMarshaller")
    def test_PebbleMessageService_02_Send_Status_To_Marshaller(self, mock_status):
        sender = Mock()
        type = Mock()
        self.outgoingPebbleMessageService.sendStatusToMarshaller(sender, type)
        self.assertTrue(mock_status.called)
        mock_status.assert_called_with(sender, type)

    @patch("services.OutgoingPebbleMessageService.OutgoingPebbleMessageService.sendMessageToMarshaller")
    @patch("services.OutgoingPebbleMessageService.OutgoingPebbleMessageService.sendDeliveryStatusToMarshaller")
    def test_PebbleMessageService_03_Send_Delivery_Status_To_Marshaller(self, mock_status, mock_send):
        transactionId = Mock()
        deliveryStatus = Mock()
        self.outgoingPebbleMessageService.sendDeliveryStatusToMarshaller(transactionId, deliveryStatus)
        self.assertTrue(mock_status.called)
        mock_status.assert_called_with(transactionId, deliveryStatus)

    @patch("data.PebbleEnvelope.pebblePushMessage")
    @patch("data.PebbleEnvelope.pebblePushMessage.readyMessage")
    @patch("services.OutgoingPebbleMessageService.OutgoingPebbleMessageService.sendMessageToMarshaller")
    def test_PebbleMessageService_04_Send_Push_Message_To_Marshaller(self, mock_send, mock_ready_message, mock_envelope):
        pushMessage = Mock()
        envelope = Mock()
        mock_envelope.return_value = envelope
        self.outgoingPebbleMessageService.sendPushMessageToMarshaller(pushMessage)
        self.assertTrue(mock_send.called)
        mock_send.assert_called_with(envelope)


    @patch("data.PebbleEnvelope.pebbleListEnvelope")
    @patch("services.OutgoingPebbleMessageService.OutgoingPebbleMessageService.sendMessageToMarshaller")
    def test_PebbleMessageService_05_Send_Pebble_List_To_Marshaller(self, mock_send, mock_envelope):
        pebbleList = Mock()
        pebbleDict = Mock()
        mock_envelope.return_value = pebbleDict
        self.outgoingPebbleMessageService.sendPebbleListToMarshaller(pebbleList)
        self.assertTrue(mock_send.called)
        mock_send.assert_called_with(pebbleDict)