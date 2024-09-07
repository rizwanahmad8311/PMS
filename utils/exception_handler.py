from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handle_validation_error,
        "Http404": _handle_http404_error,
        "PermissionDenied": _handle_permission_denied_error,
        "MethodNotAllowed": _handle_method_not_allowed_error,
        "InvalidToken": _handle_invalid_token_error,
        "AuthenticationFailed": _handle_authentication_failed_error,
        "AttributeError": _handle_attribute_error,
        "KeyError": _handle_attribute_error,
        "AssertionError": _handle_assertion_error,
        "ProgrammingError": _handle_programming_error,
        "NotAuthenticated": _handle_authentication_error,
        "DoesNotExist": _handle_http404_error,
        "EmailException": _handle_email_exception,
        "NotFound": _handle_http404_error,
        "TypeError": _handle_type_error_error,
        "ValueError": _handle_type_value_error_error,
        "UnicodeDecodeError": _handle_unicode_decode_error_error,
        "UnsupportedMediaType": _handle_unsupported_media_type,
    }
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    if response is not None:
        return _handle_validation_error

    return response


def _handle_validation_error(exc, context, response):
    if not response:
        response = Response(status=status.HTTP_403_FORBIDDEN)
        response.data = {"message": "failure", "errors": [str(exc)]}
        return response
    response.data = {}
    error_messages = []
    for field, errors in exc.detail.items():
        for error in errors:
            if error.code == "required":
                error_messages.append(f"{field} is required.")
            elif error.code == "blank" or error.code == "null":
                error_messages.append(f"{field} may not be {error.code}.")
            elif error.code == "invalid" or error.code == "unique":
                error_messages.append(str(error))
            elif error.code == "max_length":
                error_messages.append((str(error)).replace("this", field))
            else:
                error_messages.append(f"{field} does not exist.")
    response.data["message"] = "failure"
    response.data["errors"] = error_messages
    return response


def _handle_http404_error(exc, context, response):
    response = Response(status=status.HTTP_404_NOT_FOUND)
    response.data = {
        "message": "failure",
        "errors": [f"{str(exc).split(' ')[0]} does not exist."],
    }
    return response


def _handle_permission_denied_error(exc, context, response):
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_method_not_allowed_error(exc, context, response):
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_invalid_token_error(exc, context, response):
    response.data = {"message": "failure", "errors": ["Token is invalid or expired"]}
    return response


def _handle_authentication_failed_error(exc, context, response):
    response.data = {"message": "failure", "errors": ["Token is invalid or expired"]}
    return response


def _handle_attribute_error(exc, context, response):
    response = Response(status=status.HTTP_400_BAD_REQUEST)
    if str(exc) == "":
        response.data = {
            "message": "failure",
            "errors": ["An attribute error occurred"],
        }
    else:
        response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_assertion_error(exc, context, response):
    response = Response(status=status.HTTP_400_BAD_REQUEST)
    response.data = {"message": "failure", "errors": ["An assertion error occurred"]}
    return response


def _handle_programming_error(exc, context, response):
    response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_authentication_error(exc, context, response):
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_type_error_error(exc, context, response):
    response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_type_value_error_error(exc, context, response):
    response = Response(status=status.HTTP_400_BAD_REQUEST)
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_unicode_decode_error_error(exc, context, response):
    response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_email_exception(exc, context, response):
    response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response


def _handle_unsupported_media_type(exc, context, response):
    response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response.data = {"message": "failure", "errors": [str(exc)]}
    return response
