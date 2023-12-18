from django.urls import path
from .views import PostAPIView, PostDetailAPIView, PostLikeAPIView, LikeAnaliticsAPIView, UserActivityAPIView

urlpatterns = [
    path("posts/", PostAPIView.as_view(), name='post_list'),
    path("posts/<int:pk>/", PostDetailAPIView.as_view(), name='post_detail'),
    path("posts/like/", PostLikeAPIView.as_view(), name='post_like'),
    path("analitics/", LikeAnaliticsAPIView.as_view(), name='analitics'),
    path("useractivity/", UserActivityAPIView.as_view(), name='useractivity'),
]
