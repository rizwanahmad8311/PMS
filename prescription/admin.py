from django.contrib import admin
from prescription.models import *


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user", "status"]
