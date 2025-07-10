import unittest
from unittest.mock import patch, MagicMock
from professionals.grpc_client import notify_status_change

class NotifyStatusChangeTestCase(unittest.TestCase):

    @patch('professionals.grpc_client.auth_pb2.UpdateRequest')
    @patch('professionals.grpc_client.auth_pb2_grpc.CreateUsersStub')
    @patch('professionals.grpc_client.grpc.insecure_channel')
    def test_notify_status_change_success(self, mock_channel, mock_stub_class, mock_update_request):
        # Setup mock stub
        mock_stub = MagicMock()
        mock_response = MagicMock()
        mock_stub.UpdateUser.return_value = mock_response
        mock_stub_class.return_value = mock_stub

        # Mock UpdateRequest return value
        mock_update_request.return_value = MagicMock()

        # Call the function
        response = notify_status_change(user_id=1)

        # Assertions
        mock_channel.assert_called_once_with('authgrpc_backend:5003')
        mock_stub_class.assert_called_once_with(mock_channel.return_value)
        mock_update_request.assert_called_once_with(userId=1)
        mock_stub.UpdateUser.assert_called_once_with(mock_update_request.return_value)
        self.assertEqual(response, mock_response)