# serializers.pyfrom rest_framework import serializers
from rest_framework import serializers
from .models import EmailHistorico
from .models import Quota
from django.contrib.auth.models import User

class EmailHistoricoserializer(serializers.ModelSerializer):
    class Meta:
        model = EmailHistorico
        fields = ['text','result','created_at']

class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = ['disponibles','procesados']

class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_superuser']
