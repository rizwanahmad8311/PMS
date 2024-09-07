from django.db import models
from django.utils import timezone
from user.models import User


class Prescription(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="prescription"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="prescription_by" , null=True, blank=True
    )
    diagnosis = models.TextField(max_length=2000, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    medicines = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.title} | {self.user.username}"

    class Meta:
        db_table = "prescription"
        ordering = ["-created_at"]
