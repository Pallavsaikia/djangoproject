from rest_framework import status
from rest_framework.response import Response


class CustomResponse:
    data = {}
    error = {}
    success = ""

    def __init__(self, success=True, data=None, error=None):
        self.data = data
        self.error = error
        self.success = success

    @property
    def get_response(self):
        return {
            'success': self.success,
            'error': self.error,
            'data': self.data
        }

        # response = {
        #     'success': self.success,
        #     'error': self.error,
        #     'data': self.data
        # }
        # if self.success:
        #     return Response(response, status=status.HTTP_200_OK)
        # else:
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
