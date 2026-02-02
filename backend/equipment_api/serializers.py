from rest_framework import serializers
from .models import UploadedDataset


class UploadedDatasetSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    raw_data = serializers.SerializerMethodField()

    class Meta:
        model = UploadedDataset
        fields = ['id', 'name', 'uploaded_at', 'row_count', 'summary', 'raw_data']

    def get_summary(self, obj):
        return obj.summary

    def get_raw_data(self, obj):
        return obj.raw_data
