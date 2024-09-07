from django.urls import path
from prescription import views

app_name = "prescription"
urlpatterns = [
    path("create/", views.CreatePrescriptionView.as_view(), name="create-prescription"),
    path("list/", views.ListPrescriptionView.as_view(), name="list-prescription"),
    path("lookup/", views.LookupPrescriptionView.as_view(), name="lookup-prescription"),
]
