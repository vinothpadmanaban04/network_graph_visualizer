from django.db import models
from django.utils import timezone

class UploadedCSV(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='uploads/')  # New field to store the uploaded file

    def __str__(self):
        return self.file_name

class GraphEdge(models.Model):
    node_from = models.CharField(max_length=100)
    node_to = models.CharField(max_length=100)
    weight = models.IntegerField(null=True, blank=True)  # Allow weight to be null
    csv_file = models.ForeignKey(UploadedCSV, on_delete=models.CASCADE, related_name='edges')

    def __str__(self):
        return f"{self.node_from} -> {self.node_to} (Weight: {self.weight})"
