from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Case, When, IntegerField
from django.contrib.auth.models import User

from .models import Post, Comment, Like
from .serializers import PostSerializer


class FeedView(APIView):
    def get(self, request):
        posts = (
            Post.objects
            .select_related('author')
            .prefetch_related(
                'comments__author',
                'comments__replies__author'
            )
            .order_by('-created_at')
        )
        data = PostSerializer(posts, many=True).data
        return Response(data)


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post,
            like_type=Like.POST
        )

        if not created:
            return Response(
                {"message": "Post already liked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Post liked successfully"},
            status=status.HTTP_201_CREATED
        )


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            comment=comment,
            like_type=Like.COMMENT
        )

        if not created:
            return Response(
                {"message": "Comment already liked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Comment liked successfully"},
            status=status.HTTP_201_CREATED
        )


class LeaderboardView(APIView):
    def get(self, request):
        last_24_hours = timezone.now() - timedelta(hours=24)

        leaderboard = (
            User.objects
            .filter(like__created_at__gte=last_24_hours)
            .annotate(
                karma=Sum(
                    Case(
                        When(like__like_type=Like.POST, then=5),
                        When(like__like_type=Like.COMMENT, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            )
            .order_by('-karma')[:5]
        )

        data = [
            {
                "username": user.username,
                "karma": user.karma or 0
            }
            for user in leaderboard
        ]

        return Response(data)
