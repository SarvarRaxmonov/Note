from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework import viewsets, filters
from .models import BlogPost, PageVisit, ViewCount, Review, Category, Author, Contact
from .serializers import (
    BlogPostSerializer,
    ReviewSerializer,
    AuthorSerializer,
    ContactSerializer,
)
from django.utils import timezone
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BlogPostFilter
from django.shortcuts import get_object_or_404
from rest_framework import generics


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
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]
    ordering = ["-created"]
    filterset_class = BlogPostFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                {
                    "additional_data": self.retrieve_additional_data(),
                    "posts": serializer.data,
                }
            )

    def retrieve_additional_data(self):
        date = timezone.now().date()
        new_users = (
            User.objects.all()
            .filter(
                date_joined__year=date.year,
                date_joined__month=date.month,
                date_joined__day=date.day,
            )
            .count()
        )
        review = ReviewSerializer(Review.objects.most_targeted_posts(), many=True)
        authors = AuthorSerializer(
            Author.objects.get_authors_with_highest_views(), many=True
        )
        representation = {
            "Categories count": Category.objects.get_category_post_counts(),
            "new posts count": BlogPost.objects.new_posts_on_current_date(),
            "total visitors": PageVisit.objects.get_today_visits_count(),
            "blog read": ViewCount.objects.get_today_read_count(),
            "Targeted posts count": review.data,
            "new users count": new_users,
            "top authors": authors.data,
        }

        return representation


class BlogPostDetailViewset(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def retrieve(self, request, pk=None, **kwargs):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(user, context={"request": request})
        related_posts = BlogPost.objects.filter(category=serializer.data["category"])[
            :2
        ]
        serializer_blogs = BlogPostSerializer(related_posts, many=True)
        return Response(
            {
                "additional_data": BlogPostViewSet().retrieve_additional_data(),
                "data": serializer.data,
                "related posts": serializer_blogs.data,
            }
        )


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def retrieve(self, request, pk=None, **kwargs):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(user, context={"request": request})
        author_posts = BlogPost.objects.filter(author=serializer.data["id"])
        serializer_blogs = BlogPostSerializer(author_posts, many=True)

        return Response(
            {
                "author_information": serializer.data,
                "blogs_of_author": serializer_blogs.data,
            }
        )


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
