from rest_framework.serializers import ModelSerializer
from base import models

class RoomSerializer(ModelSerializer):
    class Meta:
        model = models.Room
        fields = '__all__'