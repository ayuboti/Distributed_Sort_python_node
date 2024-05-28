import unittest
from unittest.mock import patch, MagicMock
import pika  # Import pika to use in references within the tests
from app.communication import send_data, receive_data

class TestCommunication(unittest.TestCase):
    @patch('app.communication.pika', autospec=True)
    def test_send_data(self, mock_pika):
        # Setup mock
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_pika.BlockingConnection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Call function
        send_data('test_queue', {'data': 'test'})

        # Asserts
        mock_pika.BlockingConnection.assert_called_once_with(pika.ConnectionParameters(host='localhost'))
        mock_channel.queue_declare.assert_called_once_with(queue='test_queue')
        mock_channel.basic_publish.assert_called_once()
        args, kwargs = mock_channel.basic_publish.call_args
        self.assertEqual(kwargs['exchange'], '')
        self.assertEqual(kwargs['routing_key'], 'test_queue')
        self.assertTrue('data' in json.loads(kwargs['body']))

    @patch('app.communication.pika', autospec=True)
    def test_receive_data(self, mock_pika):
        # Setup mock
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_pika.BlockingConnection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Define a callback function for illustration
        def mock_callback(ch, method, properties, body):
            print("Callback called")

        # Call function with the callback
        receive_data('test_queue', mock_callback)

        # Asserts
        mock_pika.BlockingConnection.assert_called_once_with(pika.ConnectionParameters(host='localhost'))
        mock_channel.queue_declare.assert_called_once_with(queue='test_queue')
        mock_channel.basic_consume.assert_called_once()
        args, kwargs = mock_channel.basic_consume.call_args
        self.assertEqual(kwargs['queue'], 'test_queue')
        self.assertEqual(kwargs['on_message_callback'], mock_callback)
        self.assertTrue(kwargs['auto_ack'])

if __name__ == '__main__':
    unittest.main()
