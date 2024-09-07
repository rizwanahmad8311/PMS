from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

id_params_swagger = openapi.Parameter(
    "id",
    in_=openapi.IN_QUERY,
    description="id",
    type=openapi.TYPE_INTEGER,
    required=False,
    format=openapi.TYPE_INTEGER,
)

def swagger_get_method_decorator(*manual_parameters):
    parameters = list(manual_parameters)
    get_decorated_view = method_decorator(
        name="get",
        decorator=swagger_auto_schema(manual_parameters=parameters),
    )
    return get_decorated_view


def swagger_post_method_decorator(*manual_parameters):
    parameters = list(manual_parameters)
    post_decorated_view = method_decorator(
        name="post",
        decorator=swagger_auto_schema(manual_parameters=parameters),
    )
    return post_decorated_view


def swagger_put_method_decorator(*manual_parameters):
    parameters = list(manual_parameters)
    put_decorated_view = method_decorator(
        name="put",
        decorator=swagger_auto_schema(
            manual_parameters=parameters,
        ),
    )
    return put_decorated_view


def swagger_delete_method_decorator():
    delete_decorated_view = method_decorator(
        name="delete",
        decorator=swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_INTEGER, format=openapi.TYPE_INTEGER
                    )
                },
            ),
        ),
    )
    return delete_decorated_view
