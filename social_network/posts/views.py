from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializers, LikeAnaliticsSerializers, UserActivitySerializers
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.db.models.functions import TruncDay
from drf_user_activity_tracker.models import ActivityLogModel


class LikeFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Like
        fields = ['date']


class PostAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class PostLikeAPIView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    permission_classes = (IsAuthenticated,)


class LikeAnaliticsAPIView(generics.ListAPIView):
    serializer_class = LikeAnaliticsSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LikeFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = (Like.objects.filter(value=1)
                 .annotate(period=TruncDay('date')).values('period')
                 .annotate(likes=Count('pk')).values('period', 'likes'))
        return query


class UserActivityAPIView(generics.ListAPIView):
    serializer_class = UserActivitySerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = ActivityLogModel.objects.filter(user_id=self.request.user.pk)
        return query
