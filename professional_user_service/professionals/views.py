from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .serializers import ProfessionalUserSerializer
from .models import ProfessionalUser
from .grpc_client import notify_status_change
from .jwt_utils import decode_jwt
from rest_framework.decorators import api_view
import grpc
from protos import hire_notification_pb2, hire_notification_pb2_grpc


class BecomeProfessionalView(APIView):
    def post(self, request):
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Authorization header missing or invalid'}, status=401)

        jwt_token = auth_header.split(' ')[1]

        try:
            user_info = decode_jwt(jwt_token)
        except Exception as e:
            return Response({'error': str(e)}, status=401)
        
        print("Decoded JWT:", user_info)

        # Fill form with JWT data
        data = request.data.copy()
        data['user_id'] = user_info.get('id')
        data['name'] = user_info.get('username')

        print("User id : ",data['user_id'])
        print("User name : ",data['name'])

        if not data['user_id'] or not data['name']:
            return Response({'error': 'Decoded JWT missing user_id or username'}, status=400)

        serializer = ProfessionalUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print("database saved by serializer")

            # Notify auth/user service
            notify_resp = notify_status_change(user_info['id'])
            if not notify_resp.user:
                return Response({
                    "warning": "Professional data saved but user service was not notified",
                    "data": serializer.data
                }, status=202)

            return Response({
                'message': 'User upgraded to professional',
                'data': serializer.data
            }, status=201)
        else:
            print("Error in serializer")
            return Response(serializer.errors, status=400)
        

@api_view(["GET"])
@require_GET
def list_professionals(request):
        
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Authorization header missing or invalid'}, status=401)

        jwt_token = auth_header.split(' ')[1]

        try:
            user_info = decode_jwt(jwt_token)
        except Exception as e:
            return Response({'error': str(e)}, status=401)
        
        print("Decoded JWT:", user_info)

        # Fill form with JWT data
        data = request.data.copy()
        data['user_id'] = user_info.get('id')
        data['name'] = user_info.get('username')

        print("User id : ",data['user_id'])
        print("User name : ",data['name'])
    
        if request.method == "GET":
            professionals = ProfessionalUser.objects.all().exclude(user_id=data['user_id']) # No filter here

            data = [
                {
                    "professional_id": user.user_id,
                    "username": user.name,
                    "service": user.service,
                    "skills": user.skills,
                    "project": user.projects,
                    "experience": user.experience,
                }
                for user in professionals
            ]
              
            return JsonResponse(data, safe=False)
        
class HireProfessionalView(APIView):
    def post(self,request):        #grpc client program
        data=request.data
        channel=grpc.insecure_channel("hire_grpc_server:5004")
        stub=hire_notification_pb2_grpc.HireServiceStub(channel)
        response=stub.SendHireRequest(hire_notification_pb2.HireRequest(
            user=data['user'],
            user_id=data['user_id'],          
            from_date=data['from_date'],
            to_date=data['to_date'],
            price=data['price'],
            message=data['message'],
            professional_id=data['professional_id'],
            professional_user=data['professional_user'],
        ))
        return Response({"message":response.message})




