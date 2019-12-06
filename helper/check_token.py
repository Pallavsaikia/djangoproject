from django.http import JsonResponse
from functools import wraps


def check_token(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.valid_token:
            return JsonResponse({"success": False,
                                 "error": {"token": "invalid token"},
                                 "data": {}})
        else:
            return function(request, *args, **kwargs)

    return wrap
