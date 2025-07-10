from rest_framework import serializers
from .models import ProfessionalUser

class ProfessionalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalUser
        fields = '__all__'
          