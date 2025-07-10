import grpc
from protos import auth_pb2, auth_pb2_grpc
from locust import HttpUser, task, between

class ProfessionalUserLoadTest(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        channel = grpc.insecure_channel('authgrpc_backend:5003')
        stub = auth_pb2_grpc.CreateUsersStub(channel)

        login_request = auth_pb2.LoginDetails(
            useremail="testuser@example.com",
            password="testpass"
        )

        response = stub.UserLogin(login_request)

        token = response.accessToken
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    @task
    def list_professionals(self):
        self.client.get("/api/professionalslist/", headers=self.headers)

    @task
    def become_professional(self):
        self.client.post("/api/professionals/", json={
            "category": "Tester",
            "service": "QA Testing",
            "experience": 2,
            "projects": "API Load Tests",
            "skills": "Locust, Pytest"
        }, headers=self.headers)
