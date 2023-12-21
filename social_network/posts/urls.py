from django.urls import path
from .views import PostAPIView, PostDetailAPIView, PostLikeAPIView, LikeAnalyticsAPIView, UserActivityAPIView

urlpatterns = [
    path("posts/", PostAPIView.as_view(), name='post_list'),
    path("posts/<int:pk>/", PostDetailAPIView.as_view(), name='post_detail'),
    path("posts/like/", PostLikeAPIView.as_view(), name='post_like'),
    path("analytics/", LikeAnalyticsAPIView.as_view(), name='analytics'),
    path("useractivity/", UserActivityAPIView.as_view(), name='useractivity'),
]
