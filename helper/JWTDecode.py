import jwt
from first_project.settings import TOKEN_KEY


class JwtDecode:
    @staticmethod
    def decode(request):
        token = request.META['HTTP_AUTHORIZATION']
        return jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])

    @staticmethod
    def encode(username):
        return jwt.encode({"username": username}, TOKEN_KEY, algorithm="HS256")

