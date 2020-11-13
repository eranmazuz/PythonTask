# Package: SocialNetwork.views
from requests import Request
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from SocialNetwork.serializers import LoginSerializer


class LoginView(APIView):
    """
    View to login user or load page to login user(For testing).
    """

    # Everyone (authenticated or not) can access this view.
    permission_classes = (AllowAny,)

    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """
        Login the user.
        :param request: The login request.
        :return: Response containing the user data.
        :exception: If the user data is not valid.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        """
        Get Emtpy log page.
        :param request: The user request to see the page.
        :return: The response with empty login fields.
        """
        serializer = self.serializer_class()
        return Response(serializer.data)
