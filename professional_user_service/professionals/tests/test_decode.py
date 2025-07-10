from django.test import SimpleTestCase
from professionals.jwt_utils import decode_jwt
import jwt
from datetime import datetime, timedelta

class DecodeJWTTestCase(SimpleTestCase):
    def setUp(self):
        self.secret = "D2DE17E9AE96981973A39FA722F96"
        self.payload = {
            "id": 1,
            "username": "testuser",
            "exp": datetime.now() + timedelta(minutes=5),
        }
        self.token = jwt.encode(self.payload, self.secret, algorithm="HS256")

    def test_decode_jwt_valid_token(self):
        result = decode_jwt(self.token)
        self.assertEqual(result["id"], self.payload["id"])
        self.assertEqual(result["username"], self.payload["username"])

    def test_decode_jwt_invalid_token(self):
        with self.assertRaises(jwt.exceptions.DecodeError):
            decode_jwt("invalid.token.value")