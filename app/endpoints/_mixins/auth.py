from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class AuthMixin(APIView):
    permission_classes = (IsAuthenticated,)

    def get_model(self):
        raise NotImplementedError()
