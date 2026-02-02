import json
from django.db import models


class UploadedDataset(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    row_count = models.PositiveIntegerField(default=0)
    summary_json = models.TextField(blank=True)
    raw_data_json = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    @property
    def summary(self):
        if not self.summary_json:
            return {}
        return json.loads(self.summary_json)

    @property
    def raw_data(self):
        if not self.raw_data_json:
            return []
        return json.loads(self.raw_data_json)
