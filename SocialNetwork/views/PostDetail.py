# Package: SocialNetwork.views

from rest_framework import permissions, generics
from rest_framework.response import Response

from SocialNetwork.models import Post
from SocialNetwork.serializers import PostSerializer


class PostDetailView(generics.RetrieveAPIView):
    """
    View to like a post or to see the post.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can see the post.

    queryset = Post.objects.all()

    def post(self, request, pk):
        """
        Request for the user to like post.
        :param request: The user request.
        :param pk: The post ID.
        :return: Response containing the post.
        """
        user = request.user  # Get the logged user.
        post = self.get_object()  # Get the post.

        if post.creator == user:
            return self.get(request, pk)  # User can't like his own posts.

        # If user like post, unlike it otherwise like the post.
        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        # Return the post information.
        return self.get(request, pk)

    def get(self, request, pk):
        """
        Get the requested post details.
        :param request: The logged user request.
        :param pk: The post ID.
        :return: Resposne containing the requested post details.
        """
        serializer = self.serializer_class(self.get_object(), context={'user': request.user})
        return Response(serializer.data)
