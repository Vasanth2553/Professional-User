
import grpc
from protos import auth_pb2, auth_pb2_grpc

USER_SERVICE_HOST = 'authgrpc_backend:5003'  # Adjust this as needed '[::]:5003'  # Adjust this as needed ([::]:accepts from any machine)

def notify_status_change(user_id):
    channel = grpc.insecure_channel(USER_SERVICE_HOST)
    stub = auth_pb2_grpc.CreateUsersStub(channel)
    
    # Construct the request
    request = auth_pb2.UpdateRequest(userId=int(user_id))
    
    # Call the method
    response = stub.UpdateUser(request)

    print(response)

    return response