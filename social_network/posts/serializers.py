from rest_framework import serializers
from .models import Post, Like
from drf_user_activity_tracker.models import ActivityLogModel


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("__all__")


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("__all__")

    def create(self, validated_data):
        like, _ = Like.objects.update_or_create(
            post=validated_data.get('post', None),
            user=validated_data.get('user', None),
            defaults={'value': validated_data.get('value')}
        )
        return like


class LikeAnaliticsSerializers(serializers.ModelSerializer):
    period = serializers.DateTimeField(format="%d.%m.%Y",)
    likes = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ("period", "likes")


class UserActivitySerializers(serializers.ModelSerializer):
    class Meta:
        model = ActivityLogModel
        fields = ("created_time", "user_id", "api", "method", "status_code")
