# Take Python obj and convert to JSON obj       (Similar with forms.py)

from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'