from django.http import JsonResponse
from rest_framework import status


def error_404(request, exception):
    response = JsonResponse(
        {"message": "failure", "errors": ["End point not found"]},
        status=status.HTTP_404_NOT_FOUND,
    )
    return response


def error_500(request):
    response = JsonResponse(
        {"message": "failure", "errors": ["Internal server error"]},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    return response
