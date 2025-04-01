from rest_framework import serializers
from .models import ViewerHistory

class ViewerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewerHistory
        fields = ['id', 'file_name', 'file_size', 'created_at']
