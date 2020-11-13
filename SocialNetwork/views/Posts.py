# Package: SocialNetwork.views

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from SocialNetwork.models import Post
from SocialNetwork.serializers import PostSerializer

class PostsView(generics.ListCreateAPIView):
    """
    View to get the posts or for user to create new post.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def perform_create(self, serializer: PostSerializer):
        """
        link the user to the post that he made when the post is created.
        :param serializer: The post serializer.
        """
        serializer.save(creator=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Get reuqest to get all the posts.
        :param request: The user request.
        :return:
        """

        # Pass the user to the serializer to mark the posts liked by the user.
        serializer = self.serializer_class(self.get_queryset(), many=True, context={'user': request.user})
        return Response(serializer.data)
