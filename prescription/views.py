from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from prescription.models import Prescription
from prescription.serializers import PrescriptionSerializer, PrescriptionLookupSerializer
from user.enums import UserRoleChoices
from user.models import User
from rest_framework.response import Response
from django.db.models import Q, Count


class CreatePrescriptionView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not request.data.get("username"):
            raise serializers.ValidationError({"username": ["username is required."]})
        username = request.data.pop("username")
        request.data["user"] = User.objects.get(username=username).id
        print(request.user)
        if request.user.username:
            request.data["created_by"] = request.user.id
            print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED, )


class ListPrescriptionView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        prescriptions = Prescription.objects.all()
        print(self.request.user)
        if self.request.user.username:
            return prescriptions.filter(created_by=self.request.user)
        return prescriptions.none()


class LookupPrescriptionView(generics.ListAPIView):
    serializer_class = PrescriptionLookupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == UserRoleChoices.DOCTOR.value:
            return Prescription.objects.annotate(
                normal=Count("status", filter=Q(status__iexact="normal")),
                critical=Count("status", filter=Q(status__iexact="critical")),
            ).filter(created_by=self.request.user)
        elif self.request.user.role == UserRoleChoices.PATIENT.value:
            return Prescription.objects.annotate(
                normal=Count("status", filter=Q(status__iexact="normal")),
                critical=Count("status", filter=Q(status__iexact="critical")),
            ).filter(user=self.request.user)
        else:
            return None
