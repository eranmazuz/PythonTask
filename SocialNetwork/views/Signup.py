# Package: SocialNetwork.views

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import RegistrationSerializer


class SignUpView(APIView):
    """
    View to register new user or load page to register user(For testing).
    """

    # Everyone (authenticated or not) can access this view.
    permission_classes = (AllowAny,)

    serializer_class = RegistrationSerializer

    def post(self, request: Request) -> Response:
        """
        Creating new user from the information given in the request.
        :param request: Registration request
        :return: Response containing the new user.
        :exception: If the user data is not valid.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        """
        Get empty registration page.
        :param request: The user request.
        :return: Response containing empty registration.
        """
        serializer = self.serializer_class()
        return Response(serializer.data)
