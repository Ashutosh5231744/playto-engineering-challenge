from django.urls import path
from .views import FeedView, PostLikeView, CommentLikeView, LeaderboardView

urlpatterns = [
    path('feed/', FeedView.as_view()),
    path('posts/<int:post_id>/like/', PostLikeView.as_view()),
    path('comments/<int:comment_id>/like/', CommentLikeView.as_view()),
    path('leaderboard/', LeaderboardView.as_view()),
]



