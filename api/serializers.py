from rest_framework import serializers
from boards.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    text = serializers.ReadOnlyField()
    is_master = serializers.ReadOnlyField()
    parent = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    update_at = serializers.ReadOnlyField()
    created_by = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'is_master', 'parent', 'created_at', 'update_at', 'created_by', 'karma']