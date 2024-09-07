from drf_yasg import openapi
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import id_params_swagger

token_swagger = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description="token",
    type=openapi.TYPE_STRING,
    required=True,
)


def get_token_swagger():
    return method_decorator(
        name="patch",
        decorator=swagger_auto_schema(manual_parameters=[token_swagger]),
    )


def get_group_id_swagger():
    return method_decorator(
        name="get",
        decorator=swagger_auto_schema(
            manual_parameters=[id_params_swagger],
        ),
    )
