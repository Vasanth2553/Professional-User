from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from professionals.models import ProfessionalUser
from unittest.mock import patch, MagicMock

class ProfessionalViewsTestCase(APITestCase):
    def setUp(self):
        # Simulate a decoded JWT payload
        self.jwt_payload = {
            'id': 1,
            'username': 'testuser'
        }

        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTAsInVzZXJuYW1lIjoiS2FydGhpayIsImlhdCI6MTc1MTQzMTc5MywiZXhwIjoxNzUyMDM2NTkzfQ.UPSglj1wXR63Ft8tZZwia8kDEGjWzQ7peUsGiz2TtRk'
        }

        self.valid_data = {
                "category": "Developer",
                "service": "Web development",
                "experience": 1,
                "projects": "CRUD operation,Doono",
                "skills": "Java,Springboot"
                }

    @patch('professionals.views.decode_jwt')
    @patch('professionals.views.notify_status_change')
    def test_become_professional_success(self, mock_notify, mock_decode):
        mock_decode.return_value = self.jwt_payload
        mock_notify.return_value.user = True

        url = reverse('become-professional')  # make sure URL name matches
        response = self.client.post(url, data=self.valid_data, **self.headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProfessionalUser.objects.filter(user_id=1).exists())
        self.assertIn('message', response.data)

    @patch('professionals.views.decode_jwt')
    def test_become_professional_invalid_jwt(self, mock_decode):
        mock_decode.side_effect = Exception("Invalid Token")

        url = reverse('become-professional')
        response = self.client.post(url, data=self.valid_data, **self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)

    @patch('professionals.views.decode_jwt')
    def test_list_professionals(self, mock_decode):
        mock_decode.return_value = self.jwt_payload

        # Create sample professionals
        ProfessionalUser.objects.create(user_id=2, name='John', category="Developer",service= "Web development",experience= 1,projects="CRUD operation,Doono",skills="Java,Springboot")
        ProfessionalUser.objects.create(user_id=3, name='Jane', category="Developer",service= "Web development",experience= 1,projects="CRUD operation,Doono",skills="Java,Springboot")
        ProfessionalUser.objects.create(user_id=1, name='testuser', category="Developer",service= "Web development",experience= 1,projects="CRUD operation,Doono",skills="Java,Springboot")  # current user, should be excluded

        url = reverse('list-professionals')
        response = self.client.get(url, **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    @patch('professionals.views.grpc.insecure_channel')
    @patch('professionals.views.hire_notification_pb2_grpc.HireServiceStub')
    def test_hire_professional(self, mock_stub_class, mock_channel):
        mock_stub = MagicMock()
        mock_response = MagicMock()
        mock_response.message = 'Hire request sent successfully'
        mock_stub.SendHireRequest.return_value = mock_response
        mock_stub_class.return_value = mock_stub

        # Define the request payload
        data = {
            'user': 'testuser',
            'user_id': 1,
            'from_date': '2025-07-10',
            'to_date': '2025-07-20',
            'price': 1500.0,
            'message': 'Please help with the plumbing',
            'professional_id': 2,
            'professional_user': 'johnsmith'
        }

        url = reverse('hire-professional')
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hire request sent successfully')