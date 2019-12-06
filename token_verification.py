import jwt
from first_project.settings import TOKEN_KEY


class TokenVerification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.check = True
        request.token_decode = {}
        try:
            token = request.META['HTTP_AUTHORIZATION']
            decode = jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])
            request.token_decode = decode
        except:
            request.check = False

        response = self.get_response(request)
        return response
