# Package: SocialNetwork.views

from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from SocialNetwork.models import User
from SocialNetwork.serializers import PostSerializer


class UserPostsView(APIView):
    """
    View to see the user posts.
    """
    permission_classes = [permissions.IsAuthenticated]  # only authenticated users can see this view.

    def get_object(self, username):
        """
        Get the requested user.
        :param username: The user username.
        :return: The user.
        :exception: Throw HTTP 404 if the user not exist.
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        """
        Return the user posts.
        :param request: The request.
        :param username: The username of the user that the logged user whats to see his posts.
        :return: Response that containing the requested user posts.
        """
        user = self.get_object(username)

        # Passing the logged user to the serializer to compute which posts the user liked.
        serializer = PostSerializer(user.posts, many=True, context={'user': request.user})
        return Response(serializer.data)
