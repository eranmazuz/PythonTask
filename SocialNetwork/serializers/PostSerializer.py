# Package: SocialNetwork.serializers

from rest_framework import serializers

from SocialNetwork.models import Post


class PostSerializer(serializers.ModelSerializer):

    # The serialized post fields
    creator = serializers.SlugRelatedField(read_only=True, slug_field='username')
    likes_count = serializers.IntegerField(read_only= True, default=0)
    is_user_like = serializers.SerializerMethodField(read_only= True) # method to check if the current user liked the post.

    def get_is_user_like(self, obj: Post) -> bool:
        """
        Check if the user liked the post.
        :param obj:
        :return:
        """
        user = self.context.get('user') # Get the user that passed to the serializer.

        if not user:
            return False  # Sometimes this method called when the serializer deserialize the data (in post requests) so a giving dummy value because it's not needed.
        return obj.likes.filter(pk=user.pk).exists()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'creator', 'likes_count', 'is_user_like']

