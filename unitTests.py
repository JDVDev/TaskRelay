import unittest
import pebble

from libpebble2.protocol import AppMessageACK, AppMessageNACK

from mock import Mock, patch, MagicMock

from libpebble2.services.appmessage import AppMessageService


from libpebble2.communication.transports import BaseTransport
from libpebble2.communication.transports.serial import SerialTransport
from libpebble2.communication import PebbleConnection

import bluetoothManager, mainRoutine

from data import pebbleEnvelope

from factories import pebbleConnectionFactory, messageServiceFactory
from libpebble2.protocol.appmessage import AppMessage, AppMessagePush
from services import openAppService, reconnectionService, messageMarshallerService, pebbleMessageService, serverMessageService
import webserviceClient

class unitTests():  
    pebbleConnectionMock = None;
    pebble = None;
    mock_connection = None
    
    @patch("pebbleManager.pebbleManager")
    @patch("services.serverMessageService.serverMessageService")
    @patch("services.pebbleMessageService.pebbleMessageService")
    @patch('services.messageMarshallerService.messageMarshallerService')
    @patch( 'factories.pebbleConnectionFactory.PebbleConnectionFactory', autospec=True )
    @patch( 'factories.messageServiceFactory.messageServiceFactory', autospec=True)      
    def setUp(self, mock_msgFactory, mock_conFactory, mock_marshaller, mock_pebbleMsgServ, mock_serverMsgServ, mock_pebbleManager):
        self.mock_conFactory = mock_conFactory
        self.mock_msgFactory = mock_msgFactory
        self.mock_marshaller = mock_marshaller
        self.mock_pebbleMsgServ = mock_pebbleMsgServ
        self.mock_serverMsgServ = mock_serverMsgServ
        self.mock_pebbleManager = mock_pebbleManager
        self.mock_connection = Mock()
        self.mock_msgService = Mock()
        self.mock_openAppService = Mock()
        
        mock_conFactory.produceSerial.return_value = self.mock_connection
        mock_msgFactory.produceAppMessageService.return_value = self.mock_msgService
        
        self.pebbleName = '5471'
        self.pebble = pebble.pebble(self.pebbleName, mock_conFactory, mock_msgFactory, self.mock_openAppService, self.mock_pebbleMsgServ, mock_pebbleManager);
    
        self.mock_marshaller._createServerMessageService.return_value = self.mock_serverMsgServ
        self.mock_marshaller._createPebbleMessageService.return_value = self.mock_pebbleMsgServ

    
    def storeCallback(self, messageType, callback):
        self.messageCallback = callback
    #Construction
    
    #Handling
    
    #Destruction
    
    def test_01_constructs_pebble_object(self):
        print("test 01")
        print("testing pebble name initialisation")
        self.assertEqual(self.pebbleName, self.pebble.name)  
    
    def test_02_pebble_connect(self):
        print("test 02")
        self.pebble.connect()       
        #self.assertEqual(self.mock_factory.name, self.pebble.name)
        print("testing pebbleConnection production")
        self.assertTrue(self.mock_conFactory.produceSerial.called)
       
        self.mock_conFactory.produceSerial.assert_called_with(self.pebble.name)
        
        self.assertTrue(self.mock_connection.connect.called)
        self.assertTrue(self.mock_connection.run_async.called)
    
    @patch('pebble.pebble.retrySendingMessage')
    def test_03_start_appmsg_service(self, mock_retry):
        print("test 03")
        messageACK = Mock()
        messageNACK = Mock()
        messageACK.data = AppMessageACK() 
        messageNACK.data = AppMessageNACK()    
        
        self.pebble.connect()
        
        self.mock_connection.register_endpoint.side_effect = ( self.storeCallback )
        
        self.pebble.startAppMessageService()
               
        self.assertTrue(self.mock_msgFactory.produceAppMessageService.called)
        self.assertTrue(self.mock_connection.register_endpoint.called)    
             
        self.messageCallback(messageACK)
        self.assertFalse(mock_retry.called)
        self.messageCallback(messageNACK)
        self.assertTrue(mock_retry.called)
        
    def test_04_send_appmsg(self):
        print("test 04")
        self.pebble.connect()
        
        self.pebble.startAppMessageService()
        print("testing production of message")
        testMsgString = "test"
        self.pebble.sendAppMessage(testMsgString)

        self.mock_msgFactory.produceAppMessage.assert_called_with(testMsgString)
        
        print("testing sending")
        self.assertTrue(self.mock_msgService.send_message.called)
        #assert call met goede message
        
            
    def test_05_calls_reconnection_service_after_first_retry(self):
        print("test 05")
        message = Mock()
        self.pebble.connect()
        self.mock_connection.register_endpoint.side_effect = ( self.storeCallback )
        
        self.pebble.startAppMessageService()
        messageNACK = Mock()
        messageNACK.data = AppMessageNACK()      
        self.messageCallback(messageNACK)
        #self.assertFalse(mock_reconnection.called)
        self.pebble.sendAppMessage("test")
        
        self.pebble.retrySendingMessage()
        self.messageCallback(messageNACK)
        #self.assertTrue(reconnectionService.reconnectionService.__init__.called)   

    def test_06_handle_incoming_message(self):
        print('testing incoming appmessage push')
        AppMsgMock = Mock()
        AppMsgMock.data = AppMessagePush()
        
        self.pebble.connect()
        self.mock_connection.register_endpoint.side_effect = ( self.storeCallback )        
        self.pebble.startAppMessageService()
        self.messageCallback(AppMsgMock)
        self.assertTrue(self.mock_pebbleMsgServ.sendPushMessageToMarshaller.called)

    def test_07_message_marshaller_send_to_server(self):
        self.mock_marshaller._createServerMessageService()
        self.mock_marshaller.sendMessageToServer("test")
        self.assertTrue(self.mock_marshaller.sendMessageToServer.called)
        
    def test_08_message_marshaller_send_to_pebble(self):
        print("test 08: message handler Send")
        
        self.mock_marshaller._createPebbleMessageService()
        self.mock_marshaller.sendMessageToPebble("test")
        self.assertTrue(self.mock_marshaller.sendMessageToPebble.called)
        
    def test_09_read_message_from_pebble(self):
        print("test 09")
        mockAccept = MagicMock()
        mockDecline = MagicMock()
        mockAccept.data.dictionary[0].key = 1
        mockDecline.data.dictionary[0].key = 2
        
        print("testing accept from pebble")
        testPushMessage = pebbleEnvelope.pebblePushMessage("5471", mockAccept)
        self.assertEqual("Accepted", testPushMessage.message)
        
        print("testing decline from pebble")
        testPushMessage = pebbleEnvelope.pebblePushMessage("5471", mockDecline)
        self.assertEqual("Declined", testPushMessage.message)
       
    def test_10_register_and_unregister_pebbles(self):
        print("test 10")
        self.pebble.connect()
        self.assertTrue(self.mock_pebbleManager.registerPebble.called)
        
        self.pebble.disconnect()
        self.assertTrue(self.mock_pebbleManager.unregisterPebble.called)
    
    def test_11_bluetooth_manager(self):
        paired = ['3142', 'AFC4', '5471', '623D']
        connected = ['5471', 'AFC4', '623D']
        print(bluetoothManager.BluetoothManager.checkAvailabilityOfPairedPebbles(paired, connected))

    def test_12_main_routine(self):
        main = mainRoutine.mainRoutine()
    
"""   
    @patch('webserviceClient.webserviceClient.connectToService')
    def test_09_webservice_client(self, mock_connect):
        print("testing webservice client")
        testClient = webserviceClient()
        mockSock = Mock()
        mock_connect.return_value = mockSock
        testClient.connectToService()
"""