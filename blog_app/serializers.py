from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, instance):
        """Method to get replies of a comment."""
        serializer = CommentSerializer(instance.replies.all(), many=True)
        return serializer.data