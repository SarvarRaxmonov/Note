from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework import viewsets, filters
from .models import BlogPostModel, ReviewModel, CategoryModel
from .serializers import (
    BlogPostSerializer,
    ReviewModelSerializer,
    CategoryModelSerializer,
    TagModelSerializer,
    BlogSerializer
)
from django.utils import timezone
from django.contrib.auth.models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPostModel.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["category", "title"]

    def list(self, request, *args, **kwargs):
        most_recent_posts = self.queryset.order_by("-date_time")
        most_targetted_posts = ReviewModel.objects.all().order_by("-review_score")[:2]
        categories = CategoryModel.objects.all()
        date = timezone.now().date()
        today_updates_post = self.queryset.filter(
            date_time__year=date.year,
            date_time__month=date.month,
            date_time__day=date.day,
        ).count()
        new_users = (
            User.objects.all()
            .filter(
                date_joined__year=date.year,
                date_joined__month=date.month,
                date_joined__day=date.day,
            )
            .count()
        )
        post = self.get_serializer(most_recent_posts, many=True)
        targetted_posts = ReviewModelSerializer(most_targetted_posts, many=True)
        category_counts = CategoryModelSerializer(categories, many=True)

        return Response(
            {
                "targetted_posts": targetted_posts.data,
                "category_counts": category_counts.data[0]["Categories count"],
                "today's update": {
                    "posts": today_updates_post,
                    "New subscribers": new_users,
                },
                "post": post.data,
            }
        )



class BlogListCreateView(generics.ListCreateAPIView):
    queryset = BlogPostModel.objects.all()
    serializer_class = BlogSerializer

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPostModel.objects.all()
    serializer_class = BlogSerializer



    