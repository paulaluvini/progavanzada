# serializers.pyfrom rest_framework import serializers
from rest_framework import serializers
from .models import EmailHistorico

class EmailHistoricoserializer(serializers.ModelSerializer):
    class Meta:
        model = EmailHistorico
        fields = '__all__'
